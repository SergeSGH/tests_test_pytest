import subprocess

import pytest


try:
    import user as user_code
except ImportError:
    pass

output = subprocess.getoutput('user.py')

# проверяем также вывод, поскольку это указано в задании


@pytest.fixture
def data_records():
    data = []
    data.append(("Михаил Булгаков", "2-03-27", "15.05.1891",
                 "Россия, Москва, Большая Пироговская, дом 35б, кв. 6"))
    data.append(("Владимир Маяковский", "73-88", "19.07.1893",
                 "Россия, Москва, Лубянский проезд, д. 3, кв. 12"))
    return data


class MsgError:

    def __init__(self, method_name, *args, **kwargs):
        self.result = getattr(self, method_name)(*args, **kwargs)

    def add_class(self, class_name):
        text = f'Добавьте класс `{class_name}`'
        return text

    def add_method(self, method_name, class_name):
        return f'Добавьте метод `{method_name}()` для класса `{class_name}`'

    def add_attr(self, attr_name, class_name):
        return f'Добавьте свойство `{attr_name}` классу `{class_name}`'

    def wrong_attr(self, attr_name, class_name, msg=''):
        return f'Неверное значение свойства `{attr_name}` у класса `{class_name}`{msg}'

    def check_contact(self, contact_name):
        return f'`В выводе нет контакта `{contact_name}`'

    def check_contact_output(self, contact_name):
        return (f'`Вывод информации для контакта `{contact_name}` должен'
                ' точно соответствовать исходному формату')


@pytest.fixture
def msg_err():
    def _msg_err(msg_name, *args, **kwargs):
        msg = MsgError(msg_name, *args, **kwargs)
        return msg.result
    return _msg_err


class TestContact:
    init_records = [("Михаил Булгаков", "2-03-27", "15.05.1891",
                     "Россия, Москва, Большая Пироговская, дом 35б, кв. 6"),
                    ("Владимир Маяковский", "73-88", "19.07.1893",
                     "Россия, Москва, Лубянский проезд, д. 3, кв. 12")]

    correct_output = [{'contact': "Михаил Булгаков",
                       'output': ("Михаил Булгаков — адрес: Россия, Москва, Большая Пироговская,"
                                  " дом 35б, кв. 6, телефон: 2-03-27, день рождения: 15.05.1891")},
                      {'contact': "Владимир Маяковский",
                       'output': ("Владимир Маяковский — адрес: Россия, Москва, Лубянский проезд,"
                                  " д. 3, кв. 12, телефон: 73-88, день рождения: 19.07.1893")}]

    def test_init(self, msg_err):
        assert hasattr(user_code, 'Contact'), msg_err('add_class', 'Contact')

    @pytest.mark.parametrize("args", init_records)
    def test_attrs(self, args, msg_err):
        contact = user_code.Contact(*args)
        assert hasattr(contact, 'name'), msg_err('add_attr', 'name', 'Contact')
        assert contact.name == args[0], msg_err('wrong_attr', 'name', 'Contact')
        assert hasattr(contact, 'phone'), msg_err('add_attr', 'phone', 'Contact')
        assert contact.phone == args[1], msg_err('wrong_attr', 'phone', 'Contact')
        assert hasattr(contact, 'birthday'), msg_err('add_attr', 'birthday', 'Contact')
        assert contact.birthday == args[2], msg_err('wrong_attr', 'birthday', 'Contact')
        assert hasattr(contact, 'address'), msg_err('add_attr', 'address', 'Contact')
        assert contact.address == args[3], msg_err('wrong_attr', 'address', 'Contact')

    def test_has_method(self, msg_err):
        assert hasattr(
            user_code.Contact, 'show_contact'
        ), msg_err('add_method', 'show_contact', 'Contact')

    @pytest.mark.parametrize("kwargs", correct_output)
    def test_show_contact(self, kwargs, msg_err):
        assert kwargs['contact'] in output, msg_err('check_contact', kwargs['contact'])
        assert kwargs['output'] in output, msg_err('check_contact_output', kwargs['contact'])
