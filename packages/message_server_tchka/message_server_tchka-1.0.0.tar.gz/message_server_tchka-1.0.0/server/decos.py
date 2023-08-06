import logging
import sys
import traceback
import time

import log.config.server_log_config
import log.config.client_log_config

if sys.argv[0].find('server_oop') == -1:
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')

"""
Декоратор-функция для метода
"""


def mod_for_method(func):
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        print('test')
        LOGGER.debug(
            f'{time.ctime(time.time())} функция {func.__name__} c параметрами {args[1:]} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}.', stacklevel=2)

        return return_value

    return wrapper


"""
Декоратор-класс для метода
"""


class ModMethod:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            """Обертка"""
            return_value = func(*args, **kwargs)
            LOGGER.debug(
                f'{time.ctime(time.time())} функция {func.__name__} c параметрами {args[1:]} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}.', stacklevel=2)

            return return_value

        return wrapper


"""
Декоратор-функция для класса
"""


def mod_for_class(cls):
    def decorator(method):
        def new_method(self, *args, **kwargs):
            method(*args, **kwargs)

        return new_method

    cls.process_client_mess = decorator(cls.process_client_mess)
    return cls


"""
Декоратор-класс для класса
"""


class Mod:

    def __call__(self, cls):
        cls.process_client_mess = self.decorated(cls, cls.process_client_mess)
        return cls

    def decorated(self, cls, method, *args, **kwargs):
        new_method = method(self, *args, **kwargs)
        return new_method
