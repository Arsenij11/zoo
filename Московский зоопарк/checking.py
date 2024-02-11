from config import questions_answers, zoo
import telebot

class keyisnotexist(Exception):
    pass

class counterror(Exception):
    pass

class emailerror(Exception):
    pass

class checking:
    @staticmethod
    def find_key(dictionary, value):
        for key, val in dictionary.items():
            if key == value:
                return key
        return None

    @staticmethod
    def get_value(dictionary):
        b = ""
        for key, val in dictionary.items():
            a = f"{key}) {val}\n"
            b += a
        return b

class currencychecking:
    @staticmethod
    def convert_01(message: telebot.types.Message):
        try:
            key = checking.find_key(questions_answers.answers_1, message.text.lower())
            if key is None:
                raise keyisnotexist
        except keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def convert_02(message: telebot.types.Message):
        try:
            key = checking.find_key(questions_answers.answers_2, message.text.lower())
            if key is None:
                raise keyisnotexist
        except keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def convert_03(message: telebot.types.Message):
        try:
            key = checking.find_key(questions_answers.answers_3, message.text.lower())
            if key is None:
                raise keyisnotexist
        except keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error
    @staticmethod
    def convert_04(message: telebot.types.Message):
        try:
            key = checking.find_key(questions_answers.answers_4, message.text.lower())
            if key is None:
                raise keyisnotexist
        except keyisnotexist as error:
            return key, error
        else:
            error = None
            return key, error

    @staticmethod
    def animal(user_answers):
        count = {'Капибара': 0, 'Манул': 0, 'Большой тукан': 0, 'Сине-жёлтый ара': 0, 'Степной орёл': 0, 'Выдра': 0,
                 'Камышовый кот': 0}

        for i in range(len(user_answers)):
            if user_answers[i] in zoo.capybara[i]:
                count['Капибара'] += 1
            if user_answers[i] in zoo.manul[i]:
                count['Манул'] += 1
            if user_answers[i] in zoo.giant_toucan[i]:
                count['Большой тукан'] += 1
            if user_answers[i] in zoo.blue_and_gold_macaw[i]:
                count['Сине-жёлтый ара'] += 1
            if user_answers[i] in zoo.steppe_eagle[i]:
                count['Степной орёл'] += 1
            if user_answers[i] in zoo.otter[i]:
                count['Выдра'] += 1
            if user_answers[i] in zoo.jungle_cat[i]:
                count['Камышовый кот'] += 1

        print(count)

        max_key = None
        max_value = 0
        for key, value in count.items():
            if max_value < value:
                max_value = value
                max_key = key

        return max_key

    @staticmethod
    def check_personal_data(message_text):
        try:
            if len(message_text) != 5:
                raise counterror
            if '@' not in message_text[4] or '.' not in message_text[4]:
                raise emailerror
            age = int(message_text[2])
        except counterror as error:
            return error
        except ValueError as error:
            return error
        except emailerror as error:
            return error
        else:
            error = None
            return error


