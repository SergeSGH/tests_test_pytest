import random

import pytest

try:
    import user as user_code
except ImportError:
    pass

# предполагаем, что вывод пользователя output не нужен - проверяем только функцию


class MsgError:  # вывод сообщения в зависимости от типа ошибки

    def __init__(self, method_name, *args, **kwargs):
        self.result = getattr(self, method_name)(*args, **kwargs)

    def method_exist(self, method_name):
        return f'Проверьте не удалена ли функция `{method_name} в исходном коде`'

    def method_correct(self, method_name):
        return f'Проверьте корректность работы функции `{method_name}`'


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


@pytest.fixture
def dividers():
    data = []
    for _ in range(10):
        data.append(random.randint(1, 10))
    return data


@pytest.fixture
def divisions():
    data = []
    for _ in range(10):
        data.append(random.random()*10)
    return data


class TestFunc:

    def test_make_divider_of(self, msg_err):
        assert hasattr(user_code, 'make_divider_of'), msg_err('method_exist', 'make_divider_of')

    def test_division(self, dividers, divisions, msg_err):
        for divider in dividers:
            divider_func = user_code.make_divider_of(divider)
            for division in divisions:
                assert (divider_func(division) ==
                        division/divider), msg_err('method_correct', 'make_divider_of')
