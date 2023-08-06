from logging import getLogger
import sys


# Дескриптор для описания порта:
class Port:
    SERVER_LOGGER = getLogger('server')

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            self.SERVER_LOGGER.critical(
                f'Попытка запуска сервера с указанием неподходящего порта '
                f'{value}. Допустимы адреса с 1024 до 65535.')
            sys.exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


# Дескриптор для описания IP адреса:

class IPAddr:
    SERVER_LOGGER = getLogger('server')

    def __set__(self, instance, value):
        octets_arr = value.split('.')
        ip_addr_error = False

        if value:
            if len(octets_arr) != 4:
                ip_addr_error = True
            else:
                for octet in octets_arr:
                    if (not ip_addr_error) and (not octet.isdigit() or int(octet) < 0 or int(octet) > 255):
                        ip_addr_error = True

            if ip_addr_error:
                self.SERVER_LOGGER.critical(
                    f'Попытка запуска сервера с указанием некорректным ip адресом {value}')
                sys.exit(1)

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
