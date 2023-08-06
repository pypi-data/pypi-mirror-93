import dis
from logging import getLogger

import log.config.server_log_config


# Метакласс для проверки класса сервера:
class ServerCheck(type):
    SERVER_LOGGER = getLogger('server')

    def __init__(self, instance, bases, cls_dict):

        # Используемые методы:
        methods = []
        # Атрибуты, используемые в функциях:
        attrs = []

        for func in cls_dict:

            try:
                instructions = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in methods:
                            methods.append(instruction.argval)
                    elif instruction.opname == 'LOAD_ATTR':
                        if instruction.argval not in attrs:
                            attrs.append(instruction.argval)
        print(methods)
        if 'connect' in methods:
            self.SERVER_LOGGER.critical('Использование недопустимого для серверного класса метода connect')
            raise TypeError('Использование недопустимого для серверного класса метода connect')

        print(attrs)
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Отсутствует инициализация сокета TCP.')

        super().__init__(instance, bases, cls_dict)


# Метакласс для проверки класса клиента:
class ClientCheck(type):
    def __init__(self, instance, bases, cls_dict):

        methods = []
        attrs = []

        for func in cls_dict:

            try:
                instructions = dis.get_instructions(cls_dict[func])
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in methods:
                            methods.append(instruction.argval)
                    elif instruction.opname == 'LOAD_ATTR':
                        if instruction.argval not in attrs:
                            attrs.append(instruction.argval)

        print(methods)
        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('Использование недопустимого для клиентского класса метода accept, listen')

        print(attrs)
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Отсутствует инициализация сокета TCP.')

        super().__init__(instance, bases, cls_dict)
