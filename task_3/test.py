import random
import sys
import time

import pytest

try:
    import user as user_code
except ImportError:
    pass

# предполагаем, что вывод пользователя output не нужен - проверяем только дeкораторы


class MsgError:  # вывод сообщения в зависимости от типа ошибки

    def __init__(self, method_name, *args, **kwargs):
        self.result = getattr(self, method_name)(*args, **kwargs)

    def method_exist(self, method_name):
        return f'Проверьте не удален ли декоратор `{method_name} в исходном коде`'

    def method_correct(self, method_name):
        return f'Проверьте корректность работы метода `{method_name}`'

    def is_cached(self, method_name):
        return f'Проверьте, что декоратор `{method_name}()` кэширует данные при вызове'


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


@pytest.fixture
def input_time_cache():
    data = []
    n1 = random.randint(1, 2)/10
    data.append(n1)
    data.append(random.randint(3, 4)/10)
    data.append(n1)
    return data


@pytest.fixture
def output_time_cache(input_time_cache):
    return input_time_cache[:len(input_time_cache)-1]+[0.0]


class TestFunc:
    time_args = [(0.3,), (0.1,)]

    def test_has_method_time_check(self, msg_err):
        assert hasattr(user_code, 'time_check'), msg_err('method_exist', 'time_check')

    @pytest.mark.parametrize("args", time_args)
    def test_time_check(self, args, msg_err):
        original_stdout = sys.stdout
        with open('time_check_output.txt', 'w', encoding="utf-8") as f:
            sys.stdout = f
            measured_sleep = user_code.time_check(time.sleep)
            measured_sleep(args[0])
            sys.stdout = original_stdout

        with open('time_check_output.txt', 'r', encoding="utf-8") as f:
            decorated_output = f.read()
        assert (f'Время выполнения функции: {round(float(args[0]),1)} с.'
                in decorated_output), msg_err('method_correct', 'time_check')

    def test_has_method_cache_args(self, msg_err):
        assert hasattr(user_code, 'cache_args'), msg_err('method_exist', 'cache_args')

    def test_cache_args(self, input_time_cache, output_time_cache, msg_err):
        original_stdout = sys.stdout
        with open('cache_check_output.txt', 'w', encoding="utf-8") as f:
            sys.stdout = f
            cached_sleep = user_code.time_check(user_code.cache_args(time.sleep))
            for time_par in input_time_cache:
                cached_sleep(time_par)
            sys.stdout = original_stdout

        with open('cache_check_output.txt', 'r', encoding="utf-8") as f:
            cached_output = f.read()
        row_list = cached_output.split('\n')
        for i, time_par in enumerate(output_time_cache):
            assert (f'Время выполнения функции: {round(float(time_par),1)} с.' in
                    row_list[i]), msg_err('method_correct', 'cache_args')
        assert (f'Время выполнения функции: {round(float(input_time_cache[2]),1)} с.'
                not in row_list[2]), msg_err('is_cached', 'cache_args')
