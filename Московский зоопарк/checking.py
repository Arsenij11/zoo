"""В файле checking находятся классы с методами для проверки чего-либо"""


# Импорт необходимых модулей
from config import Questions_answers, Zoo
import telebot
import random


# Собственные классы исключений
class Keyisnotexist(Exception):
    """Класс Keyisnotexist представляет собой собственный класс исключений, он вызывается, когда предоставлено больше или меньше данных."""

    pass

class Counterror(Exception):
    """Класс Counterror представляет собой собственный класс исключений, он вызывается, когда вместо возраста введено НЕ число."""

    pass

class Emailerror(Exception):
    """Класс Emailerror представляет собой собственный класс исключений, он вызывается, когда неверно введён email."""

    pass

class Emptydata(Exception):
    """Класс Emptydata представляет собой собственный класс исключений, он вызывается, когда данные после запроса в БД равны None(NULL)"""

    pass

class Smallusername(Exception):
    pass


class Largeusername(Exception):
    pass


class Smallpassword(Exception):
    pass


class Largepassword(Exception):
    pass

class Specialsymbols(Exception):
    pass

# Класс Checking
class Checking:
    """Класс Checking содержит два метода find_key и get_value"""

    @staticmethod
    def find_key(dictionary, value):
        """Статический метод  find_key вызывается, когда нужно найти нужную букву в словаре с возможными ответами.

        Если он найден, то возвращается эта буква.
        А если нет, то None.
        """

        for key, val in dictionary.items():
            if key == value:
                return key
        return None

    @staticmethod
    def get_value(dictionary):
        """Статический метод get_value вызывается, когда боту нужно отобразить возможные ответы какого-либо вопроса."""

        b = ""
        for key, val in dictionary.items():
            a = f"{key}) {val}\n"
            b += a
        return b


# Класс Currencychecking
class Currencychecking:
    """Класс Currencychecking содержит 6 методов convert_01, convert_02, convert_03, convert_04, animal, check_personal_data."""

    @staticmethod
    def convert_01(message: telebot.types.Message):
        """Здесь проверяется введённый пользователем ответ на первый вопрос.

        Если всё хорошо, то метод возвращает этот ответ.
        Если такого ответа не существует, то метод возвращает этот неправильный ответ и исключение Keyisnotexist.
        """

        try:
            key = Checking.find_key(Questions_answers.answers_1, message.text.lower())
            if key is None:
                raise Keyisnotexist
        except Keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def convert_02(message: telebot.types.Message):
        """Здесь проверяется введённый пользователем ответ на второй вопрос.

            Если всё хорошо, то метод возвращает этот ответ.
            Если такого ответа не существует, то метод возвращает этот неправильный ответ и исключение Keyisnotexist.
        """

        try:
            key = Checking.find_key(Questions_answers.answers_2, message.text.lower())
            if key is None:
                raise Keyisnotexist
        except Keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def convert_03(message: telebot.types.Message):
        """Здесь проверяется введённый пользователем ответ на третий вопрос.

            Если всё хорошо, то метод возвращает этот ответ.
            Если такого ответа не существует, то метод возвращает этот неправильный ответ и исключение Keyisnotexist.
        """

        try:
            key = Checking.find_key(Questions_answers.answers_3, message.text.lower())
            if key is None:
                raise Keyisnotexist
        except Keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error
    @staticmethod
    def convert_04(message: telebot.types.Message):
        """Здесь проверяется введённый пользователем ответ на четвёртый вопрос.

            Если всё хорошо, то метод возвращает этот ответ.
            Если такого ответа не существует, то метод возвращает этот неправильный ответ и исключение Keyisnotexist.
        """

        try:
            key = Checking.find_key(Questions_answers.answers_4, message.text.lower())
            if key is None:
                raise Keyisnotexist
        except Keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def animal(user_answers):
        """В этом методе ведётся подсчёт результатов.

        Сначала инициализируется словарь count.
        Затем происходит подсчёт результатов, если ответ есть в списках переменных класса config.Zoo, то к значению соответствующего ключа прибавляется единица.
        Далее происходит сам подсчёт результатов в цикле for key, value in count.items().
        Если был найден наибольший показатель в словаре, то метод возвращает соответствующий ключ.
        Если же было найдено несколько ключей с одинаковым количеством максимальных значений, то эти ключи добавляются в список max_key_list, перемешиваются, и оттуда рандомно выбирается один, и этот ключ возвращает метод.
        """

        # Словарь для подсчёта результатов
        count = {'Капибара': 0, 'Манул': 0, 'Большой тукан': 0, 'Сине-жёлтый ара': 0, 'Степной орёл': 0, 'Выдра': 0,
                 'Камышовый кот': 0}

        # Подсчёт результатов
        for i in range(len(user_answers)):
            if user_answers[i] in Zoo.capybara[i]:
                count['Капибара'] += 1
            if user_answers[i] in Zoo.manul[i]:
                count['Манул'] += 1
            if user_answers[i] in Zoo.giant_toucan[i]:
                count['Большой тукан'] += 1
            if user_answers[i] in Zoo.blue_and_gold_macaw[i]:
                count['Сине-жёлтый ара'] += 1
            if user_answers[i] in Zoo.steppe_eagle[i]:
                count['Степной орёл'] += 1
            if user_answers[i] in Zoo.otter[i]:
                count['Выдра'] += 1
            if user_answers[i] in Zoo.jungle_cat[i]:
                count['Камышовый кот'] += 1

        print(count)

        # Определение победителя
        max_key = None
        max_value = 0
        max_key_list = []
        last_max_key = None
        for key, value in count.items():
            if max_value < value:
                max_value = value
                max_key = key
                last_max_key = key
                if len(max_key_list) > 0:
                    for max in range(len(max_key_list)):
                        max_key_list.pop()
            elif max_value == value:
                max_key_list.append(key)
                if last_max_key is not None and last_max_key not in max_key_list:
                    max_key_list.append(last_max_key)
        if len(max_key_list) > 0:
            random.shuffle(max_key_list)
            random_key = random.choice(max_key_list)
            return random_key
        else:
            return max_key

    @staticmethod
    def check_personal_data(message_text):
        """В этом методе происходит проверка на правильность введённых персональных данных.

        В случае, если предоставлено больше или меньше данных, то к переменной error присваивается исключение Counterror.
        В случае, если вместо возраста введено НЕ число, то к переменной error присваивается исключение ValueError.
        В случае, если неверно введён email, то к переменной error присваивается исключение Emailerror.
        В случае, если всё хорошо, то к переменной error приравнивается None.
        """
        try:
            if len(message_text) != 5:
                raise Counterror
            if '@' not in message_text[4] or '.' not in message_text[4]:
                raise Emailerror
            age = int(message_text[2])
        except Counterror as error:
            return error
        except ValueError as error:
            return error
        except Emailerror as error:
            return error
        else:
            error = None
            return error

    @staticmethod
    def check_username(message_text):
        try:
            banned_symbols = ['%', '@', '#', '$', '&', '*', "+", "—", "/", "\\", "|", "~", "^", "=", "-"]
            if len(message_text) < 10:
                raise Smallusername
            if len(message_text) > 30:
                raise Largeusername
            for i in banned_symbols:
                if i in message_text:
                    raise Specialsymbols
        except Smallusername as error:
            return error
        except Largeusername as error:
            return error
        except Specialsymbols as error:
            return error
        else:
            error = None
            return error

    @staticmethod
    def check_password(message_text):
        try:
            banned_symbols = ['%', '@', '#', '$', '&', '*', "+", "—", "/", "\\", "|", "~", "^", "=", "-"]
            if len(message_text) < 10:
                raise Smallpassword
            if len(message_text) > 20:
                raise Largepassword
            for i in banned_symbols:
                if i in message_text:
                    raise Specialsymbols
        except Smallpassword as error:
            return error
        except Largepassword as error:
            return error
        except Specialsymbols as error:
            return error
        else:
            error = None
            return error
