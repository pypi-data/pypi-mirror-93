import binascii
import configparser
import hmac
import os
import socket
import sys
import argparse
import select
import json
import time
from logging import getLogger
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from common_oop import CommonApi
from decos import ModMethod
import log.config.server_log_config
from metaclasses import ServerCheck
from descriptors import Port, IPAddr
from database import ServerStorage
from main_window import MainWindow

new_connection = False
conflag_lock = threading.Lock()


# @mod_for_class
# @Mod()
class Server(CommonApi, threading.Thread, metaclass=ServerCheck):
    listen_port = Port()
    listen_address = IPAddr()

    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self.clients = []
        self.messages = []
        self.names = dict()
        self.sock = None
        self.listen_socks = None
        self.error_socks = None
        self.running = True

        self.config = configparser.ConfigParser()
        self.dir_path = os.getcwd()
        self.config.read(f"{self.dir_path}/{'server.ini'}")

        if not 'SETTINGS' in self.config:
            self.config.add_section('SETTINGS')
            self.config.set('SETTINGS', 'Default_port', str(self.DEFAULT_PORT))
            self.config.set('SETTINGS', 'Listen_Address', '')
            self.config.set('SETTINGS', 'Database_path', '')
            self.config.set('SETTINGS', 'Database_file', 'server_database.db3')

        parser = argparse.ArgumentParser()
        parser.add_argument('-p', default=self.config['SETTINGS']['Default_port'], type=int, nargs='?')
        parser.add_argument('-a', default=self.config['SETTINGS']['Listen_Address'], nargs='?')
        parser.add_argument('--no_gui', action='store_true')
        namespace = parser.parse_args(sys.argv[1:])
        self.listen_address = namespace.a
        self.listen_port = namespace.p
        self.gui_flag = namespace.no_gui

        self.database = ServerStorage(
            os.path.join(
                self.config['SETTINGS']['Database_path'],
                self.config['SETTINGS']['Database_file']))

    SERVER_LOGGER = getLogger('server')

    @ModMethod()
    def process_client_mess(self, message_dict, client):
        '''
        Фукция принимает словарь - сообщение от клиента, проверяет корректность данных и формирует словарь - ответ клиенту.
        :return:
        '''

        global new_connection
        self.SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message_dict}')

        # для сообщения о присутствии
        if self.ACTION in message_dict and message_dict[self.ACTION] == self.PRESENSE and \
                self.TIME in message_dict and self.USER in message_dict:
            self.autorize_user(message_dict, client)

        # для обычного сообщения
        elif self.ACTION in message_dict and message_dict[self.ACTION] == self.MESSAGE and \
                self.DESTINATION in message_dict and self.TIME in message_dict and \
                self.SENDER in message_dict and self.MESSAGE_TEXT in message_dict and \
                self.names[message_dict[self.SENDER]] == client:
            if message_dict[self.DESTINATION] in self.names:
                self.database.process_message(message_dict[self.SENDER], message_dict[self.DESTINATION])
                self.process_message(message_dict)
                response = self.RESPONSE_200
                try:
                    self.send_mess(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = self.RESPONSE_400
                response[self.ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    self.send_mess(client, response)
                except OSError:
                    pass
            return


        # для сообщения  выходе
        elif self.ACTION in message_dict and message_dict[self.ACTION] == self.EXIT and \
                self.ACCOUNT_NAME in message_dict and self.names[message_dict[self.ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # для запроса контакт-листа
        elif self.ACTION in message_dict and message_dict[
            self.ACTION] == self.GET_CONTACTS and self.USER in message_dict and \
                self.names[message_dict[self.USER]] == client:
            response = self.RESPONSE_202
            response[self.LIST_INFO] = self.database.get_contacts(message_dict[self.USER])
            try:
                self.send_mess(client, response)
            except OSError:
                self.remove_client(client)

        # для добавления контакта
        elif self.ACTION in message_dict and message_dict[
            self.ACTION] == self.ADD_CONTACT and self.ACCOUNT_NAME in message_dict and \
                self.USER in message_dict and self.names[message_dict[self.USER]] == client:
            self.database.add_contact(message_dict[self.USER], message_dict[self.ACCOUNT_NAME])
            try:
                self.send_mess(client, self.RESPONSE_200)
            except OSError:
                self.remove_client(client)


        # для удаления контакта
        elif self.ACTION in message_dict and message_dict[
            self.ACTION] == self.REMOVE_CONTACT and self.ACCOUNT_NAME in message_dict \
                and self.USER in message_dict \
                and self.names[message_dict[self.USER]] == client:
            self.database.remove_contact(message_dict[self.USER], message_dict[self.ACCOUNT_NAME])
            try:
                self.send_mess(client, self.RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # для запроса всех пользователей
        elif self.ACTION in message_dict and message_dict[
            self.ACTION] == self.USERS_REQUEST and self.ACCOUNT_NAME in message_dict \
                and self.names[message_dict[self.ACCOUNT_NAME]] == client:
            response = self.RESPONSE_202
            response[self.LIST_INFO] = [user[0] for user in self.database.users_list()]
            try:
                self.send_mess(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif self.ACTION in message_dict and message_dict[
            self.ACTION] == self.PUBLIC_KEY_REQUEST and self.ACCOUNT_NAME in message_dict:
            response = self.RESPONSE_511
            response[self.DATA] = self.database.get_pubkey(message_dict[self.ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[self.DATA]:
                try:
                    self.send_mess(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = self.RESPONSE_400
                response[self.ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    self.send_mess(client, response)
                except OSError:
                    self.remove_client(client)


        else:
            response = self.RESPONSE_400
            response[self.ERROR] = 'Запрос некорректен.'
            try:
                self.send_mess(client, response)
            except OSError:
                self.remove_client(client)

    @ModMethod()
    def process_message(self, message_dict):
        """
        Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
        список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
        :param message:
        :param names:
        :param listen_socks:
        :return:
        """


        if message_dict[self.DESTINATION] in self.names and self.names[message_dict[self.DESTINATION]] in self.listen_socks:

            try:
                self.send_mess(self.names[message_dict[self.DESTINATION]], message_dict)
                self.SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message_dict[self.DESTINATION]} '
                                        f'от пользователя {message_dict[self.SENDER]}.')

            except OSError:
                self.remove_client(message_dict[self.DESTINATION])
        elif message_dict[self.DESTINATION] in self.names and self.names[
            message_dict[self.DESTINATION]] not in self.listen_socks:
            self.SERVER_LOGGER.error(
                f'Связь с клиентом {message_dict[self.DESTINATION]} была потеряна. Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message_dict[self.DESTINATION]])
        else:
            self.SERVER_LOGGER.error(
                f'Пользователь {message_dict[self.DESTINATION]} не зарегистрирован')

    def print_help(self):
        print('Поддерживаемые комманды:')
        print('users - список пользователей')
        print('connected - список пользователей online')
        print('loghist - история входов пользователя')
        print('exit - завершение работы сервера.')
        print('help - вывод справки по поддерживаемым командам')

    def autorize_user(self, message_dict, sock):
        '''Метод реализующий авторизцию пользователей.'''
        # Если имя пользователя уже занято то возвращаем 400
        self.SERVER_LOGGER.debug(f'Start auth process for {message_dict[self.USER]}')
        if message_dict[self.USER][self.ACCOUNT_NAME] in self.names.keys():
            response = self.RESPONSE_400
            response[self.ERROR] = 'Имя пользователя уже занято.'
            try:
                self.SERVER_LOGGER.debug(f'Username busy, sending {response}')
                self.send_mess(sock, response)
            except OSError:
                self.SERVER_LOGGER.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message_dict[self.USER][self.ACCOUNT_NAME]):
            response = self.RESPONSE_400
            response[self.ERROR] = 'Пользователь не зарегистрирован.'
            try:
                self.SERVER_LOGGER.debug(f'Unknown username, sending {response}')
                self.send_mess(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            self.SERVER_LOGGER.debug('Correct username, starting passwd check.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = self.RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[self.DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(self.database.get_hash(message_dict[self.USER][self.ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            self.SERVER_LOGGER.debug(f'Auth message = {message_auth}')
            try:
                # Обмен с клиентом
                self.send_mess(sock, message_auth)
                ans = self.get_mess(sock)
            except OSError as err:
                self.SERVER_LOGGER.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[self.DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if self.RESPONSE in ans and ans[self.RESPONSE] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message_dict[self.USER][self.ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    self.send_mess(sock, self.RESPONSE_200)
                except OSError:
                    self.remove_client(message_dict[self.USER][self.ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.database.user_login(
                    message_dict[self.USER][self.ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message_dict[self.USER][self.PUBLIC_KEY])
            else:
                response = self.RESPONSE_400
                response[self.ERROR] = 'Неверный пароль.'
                try:
                    self.send_mess(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        '''Метод реализующий отправки сервисного сообщения 205 клиентам.'''
        for client in self.names:
            try:
                self.send_mess(self.names[client], self.RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])

    def run(self):
        '''
        Загрузка параметров командной строки или параметров по умолчанию, если они не заданы
        Пример вызова скрипта из команднойстроки:
        server.py -a 10.0.0.101 -p 7766
        :return:
        '''

        self.SERVER_LOGGER.info(f'Запущен сервер, порт: {self.listen_port}, адрес: {self.listen_address}.')

        # по полученнам данным создаем сокет

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # для тестирования работы метакласса добавляем  интрукцию connect
        # transport.connect((listen_address, listen_port))

        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(0.5)

        transport.listen(self.MAX_CONNECTIONS)
        while self.running:
            # проверяем наличие клиентов, ожидающих подключения
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                self.SERVER_LOGGER.info(f'Установлено соедение с клиентом {client_address}')
                self.clients.append(client)

            recv_data_lst = []

            # создаем списки из сообщений, ожидающих обработки
            try:
                if self.clients:
                    recv_data_lst, self.listen_socks, self.error_socks = select.select(self.clients, self.clients, [], 0)
            except OSError as err:
                self.SERVER_LOGGER.error(f'Ошибка работы с сокетами: {err}')

            # принимаем сообщения
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_mess(self.get_mess(client_with_message), client_with_message)
                    except:
                        self.SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился при получении.')
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        '''
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        '''
        self.SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()


def main():
    my_server = Server()

    my_server.daemon = True
    my_server.start()

    if my_server.gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                my_server.running = False
                my_server.join()
                break

    else:
        # Графическое окуружение:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(my_server.database, my_server, my_server.config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        my_server.running = False



if __name__ == '__main__':
    main()
