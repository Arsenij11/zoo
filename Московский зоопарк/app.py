"""Это основной файл, с помощью которого запускается бот"""

# Импорт необходимых модулей, классов, функций и т.д.
import telebot
import checking
import config
import sqlite3
import logging
from Token import TOKEN
from descripton import *


# Инициализация бота
bot = telebot.TeleBot(TOKEN)


# Константы для состояний
WAITING_FOR_START = "waiting_for_start"
WAITING_FOR_ANSWER = "waiting_for_answer"
WAITING_FOR_QUESTION_1 = "waiting_for_q1"
WAITING_FOR_QUESTION_2 = "waiting_for_q2"
WAITING_FOR_QUESTION_3 = "waiting_for_q3"
WAITING_FOR_QUESTION_4 = "waiting_for_q4"
WAITING_FOR_TRY = "waiting_for_try"
WAITING_FOR_COMMENTARY = "waiting_for_com"
WAITING_FOR_PERSONAL_DATA = "waiting_for_DATA"
COMMENT = 'comment'
JUST_WAITING = 'just_waiting'
WAIT_RESULT = 'wait_result'
WAIT_PASSWORD = 'wait_password'
WAIT_USERNAME = 'wait_username'


# Словарь для хранения текущего состояния каждого пользователя
user_states = {}

# Результаты тестов
user_answers = {}
result = {}
result_img = {}


# Имя пользователя
username = {}

# Пароль
password = {}


# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler("app.log", mode='a')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)

# Начало логирования
py_logger.info('Start_logging: app.py')

# Создание таблиц
try:
    with sqlite3.connect('commets_db.SQLite') as conn:
            cursor = conn.cursor()
            cursor.executescript("""CREATE TABLE IF NOT EXISTS PERSONAL_DATA(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(100) NOT NULL, 
            surname VARCHAR(100) NOT NULL, 
            age INTEGER NOT NULL, 
            city VARCHAR(100) NOT NULL, 
            message_chat_id INTEGER NOT NULL UNIQUE, 
            email TEXT NOT NULL);


            CREATE TABLE IF NOT EXISTS RESULTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            message_chat_id INTEGER NOT NULL UNIQUE,
            answer_01 VARCHAR(1) NOT NULL, 
            answer_02 VARCHAR(1) NOT NULL, 
            answer_03 VARCHAR(1) NOT NULL, 
            answer_04 VARCHAR(1) NOT NULL, 
            result TEXT NOT NULL,
            animal BLOB NOT NULL,
            FOREIGN KEY (message_chat_id) REFERENCES PERSONAL_DATA(message_chat_id)
             );

            CREATE TABLE IF NOT EXISTS COMMENTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            message_chat_id INTEGER NOT NULL UNIQUE,
            comment TEXT NOT NULL,
            FOREIGN KEY (message_chat_id) references PERSONAL_DATA(message_chat_id));


            CREATE TABLE IF NOT EXISTS CONTACT(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            message_chat_id INTEGER NOT NULL UNIQUE,
            is_checked BOOLEAN NOT NULL DEFAULT(FALSE),
            FOREIGN KEY (message_chat_id) references PERSONAL_DATA(message_chat_id));

            CREATE TABLE IF NOT EXISTS PASSWORDS (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                message_chat_id INTEGER NOT NULL UNIQUE,
                username VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(20) NOT NULL,
                CONSTRAINT passwords_ck CHECK (
                    LENGTH(password) >= 10 AND
                    password NOT LIKE '%\%%' AND 
                    password NOT LIKE '%@%' AND 
                    password NOT LIKE '%#%' AND 
                    password NOT LIKE '%$%' AND 
                    password NOT LIKE '%&%' AND 
                    password NOT LIKE '%*%' AND 
                    password NOT LIKE '%+%' AND 
                    password NOT LIKE '%—%' AND 
                    password NOT LIKE '%/%' AND 
                    password NOT LIKE '%|%' AND 
                    password NOT LIKE '%~%' AND 
                    password NOT LIKE '%^%' AND 
                    password NOT LIKE '%=%' AND 
                    password NOT LIKE '%\\%' AND
                    password NOT LIKE '%-%'  
                ),
                CONSTRAINT username_ck CHECK (
                    LENGTH(username) >= 10 AND
                    username NOT LIKE '%\%%' AND  
                    username NOT LIKE '%@%' AND 
                    username NOT LIKE '%#%' AND 
                    username NOT LIKE '%$%' AND 
                    username NOT LIKE '%&%' AND 
                    username NOT LIKE '%*%' AND 
                    username NOT LIKE '%+%' AND 
                    username NOT LIKE '%—%' AND 
                    username NOT LIKE '%/%' AND 
                    username NOT LIKE '%|%' AND 
                    username NOT LIKE '%~%' AND 
                    username NOT LIKE '%^%' AND 
                    username NOT LIKE '%=%' AND
                    username NOT LIKE '%\\%' AND
                    username NOT LIKE '%-%'
                ),
                FOREIGN KEY (message_chat_id) REFERENCES PERSONAL_DATA(message_chat_id)
            );

            CREATE TABLE IF NOT EXISTS ACCESS(
             id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             username VARCHAR(30) NOT NULL,
             password VARCHAR(20) NOT NULL,
             message_chat_id INTEGER NOT NULL,
             is_access BOOLEAN NOT NULL DEFAULT(FALSE),
             FOREIGN KEY (username) REFERENCES PASSWORDS(username),
             FOREIGN KEY (password) REFERENCES PASSWORDS(password)
             );

            CREATE VIEW IF NOT EXISTS watch_results as
            SELECT 
            case r.answer_01
            when 'a'then 'Арбуз'
            when 'b'then 'Куриный стейк'
            when 'c'then 'Форель'
            when 'd'then 'Инжир'
            when 'e'then 'Грецкий орех'
            when 'f'then 'Морковный салат'
            end as "Ответ на первый вопрос",
            case r.answer_02
            when 'a'then 'Поплавать в бассейне'
            when 'b'then 'Затаиться в тихом месте и поспать'
            when 'c'then 'Прогуляться на свежем воздухе'
            end as "Ответ на второй вопрос",
            case r.answer_03
            when 'a'then 'Предпочитаю спать весь день'
            when 'b'then 'Утром'
            when 'c'then 'Днём'
            when 'd'then 'Вечером'
            when 'e'then 'Ночью'
            end as "Ответ на третий вопрос",
            case r.answer_04
            when 'a'then 'В одиночестве'
            when 'b'then 'С семьёй'
            when 'c'then 'С друзьями'
            end as "Ответ на четвёртый вопрос",
            r.result as "Результат", pd.message_chat_id as "ID телеграма" 
            FROM COMMENTS c
            join PERSONAL_DATA pd ON pd.message_chat_id = c.message_chat_id
            join RESULTS r ON r.message_chat_id = c.message_chat_id;


            CREATE VIEW IF NOT EXISTS "Команда /contact" as 
            SELECT pd.name as "Имя", pd.surname as "Фамилия", 
            case r.answer_01
            when 'a'then 'Арбуз'
            when 'b'then 'Куриный стейк'
            when 'c'then 'Форель'
            when 'd'then 'Инжир'
            when 'e'then 'Грецкий орех'
            when 'f'then 'Морковный салат'
            end as "Ответ на первый вопрос",
            case r.answer_02
            when 'a'then 'Поплавать в бассейне'
            when 'b'then 'Затаиться в тихом месте и поспать'
            when 'c'then 'Прогуляться на свежем воздухе'
            end as "Ответ на второй вопрос",
            case r.answer_03
            when 'a'then 'Предпочитаю спать весь день'
            when 'b'then 'Утром'
            when 'c'then 'Днём'
            when 'd'then 'Вечером'
            when 'e'then 'Ночью'
            end as "Ответ на третий вопрос",
            case r.answer_04
            when 'a'then 'В одиночестве'
            when 'b'then 'С семьёй'
            when 'c'then 'С друзьями'
            end as "Ответ на четвёртый вопрос",
            r.result as "Результат",c.comment as "Комментарий", pd.email, pd.message_chat_id
            FROM COMMENTS c
            join PERSONAL_DATA pd ON pd.message_chat_id = c.message_chat_id
            join RESULTS r ON r.message_chat_id = c.message_chat_id;


            CREATE VIEW IF NOT EXISTS Profile as 
            SELECT pd.name as "Имя", pd.surname as "Фамилия", pd.age as "Возраст",
            pd.city as "Город проживания",
            c.comment as "Комментарий", pd.email, pd.message_chat_id as "ID телеграма"
            FROM COMMENTS c
            join PERSONAL_DATA pd ON pd.message_chat_id = c.message_chat_id;
            """)
except sqlite3.Error as e:
    py_logger.error(f"Ошибка при создании таблиц: {e}")
    print(f"Ошибка при создании таблиц: {e}")
else:
    py_logger.info("Таблицы были созданы успешно!")


# Очистка результатов
def cleaning(message):
    """Очистка результатов. В списке user_answer[message.chat.id] хранятся результаты теста, в result[message.chat.id] тотемное животное, в result_img[message.chat.id] название файла с фотографией тотемного животного"""

    user_answers[message.chat.id] = []
    result[message.chat.id] = ""
    result_img[message.chat.id] = ""


# Команда Info
@bot.message_handler(commands=['info'], func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_START or user_states.get(message.chat.id) is None)
def info(message):
    """Здесь с помощью команды /info отображается основная информация по использованию бота"""

    try:
        bot.send_message(message.chat.id, INFO, parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")


# Команда start
@bot.message_handler(commands=['start'], func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_START or user_states.get(message.chat.id) is None)
def start(message):
    """Здесь с помощью команды /start отправляется сообщение с приветствием"""

    try:
        bot.send_message(message.chat.id, f"<b>Здравствуйте, {message.from_user.first_name}!</b>\n"\
         "Рады приветствовать Вас в боте-викторине, помогающему пользователю подобрать тотемное животное.\n"\
         "Чтобы узнать подробности, введите команду /info.\n"\
         "Если хотите начать, введите команду /startquiz.", parse_mode='html')
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}")
        py_logger.error(f"Ошибка со стороны сервера: {e}")


# Команда site
@bot.message_handler(commands=['site'], func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_START or user_states.get(message.chat.id) is None)
def site(message):
    try:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton('Перейти на сайт', url='https://moscowzoo.ru/my-zoo/become-a-guardian/'))
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
    else:
        bot.send_message(message.chat.id, 'Для перехода на сайт нажмите на кнопку',reply_markup=keyboard)

# Команда startquiz
@bot.message_handler(commands=['startquiz'], func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_START or user_states.get(message.chat.id) is None)
def start_quiz(message):
    """Если пользователь ввёл /startquiz, то отображается  сообщение и клавиатура с кнопками 'да'/'нет', а значение ключа с id пользователя в словаре user_states меняется на WAITING_FOR_ANSWER"""

    try:
        # Создаем клавиатуру для ответов
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Да'), telebot.types.KeyboardButton('Нет'))
        # Отправляем сообщение с вопросом и клавиатурой
        bot.send_message(message.chat.id, "Вам нужно выбрать лишь один правильный ответ (введите только букву, а не сам ответ целиком) в каждом вопросе.\nВы готовы?", reply_markup=keyboard)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
    else:
        # Устанавливаем состояние ожидания ответа после команды /startquiz
        user_states[message.chat.id] = WAITING_FOR_ANSWER


# Ожидание ответа
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_ANSWER)
def quiz(message):
    """Если значение ключа с id пользователя в словаре user_states равняется константе WAITING_FOR_ANSWER, то бот ожидает ответа 'да'/'нет', чтобы начать тест.

    В случае, если пользователь вводит 'нет', то бот отправляет соответствующее значение, а состояние id пользователя меняется на WAITING_FOR_START.
    В случае, если пользователь вводит 'да', то бот выводит клавиатуру с возможными вариантами ответа на первый вопрос, а состояние пользователя в словаре меняется на WAITING_FOR_QUESTION_1
    """

    try:
        # Обработка ответов
        if message.text.lower() == 'нет':
            bot.send_message(message.chat.id, "Ясно :(\nКак передумаете, введите /startquiz")
            # Возвращаем пользователя в начальное состояние
            user_states[message.chat.id] = WAITING_FOR_START
        elif message.text.lower() == 'да':
            user_answers[message.chat.id] = []
            bot.send_message(message.chat.id, "Отлично, тогда начнём :)")
            answer_01 = checking.Checking.get_value(config.Questions_answers.answers_1)
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton('a'), telebot.types.KeyboardButton('b'), telebot.types.KeyboardButton('c'), telebot.types.KeyboardButton('d'), telebot.types.KeyboardButton('e'), telebot.types.KeyboardButton('f'))
            bot.send_message(message.chat.id, config.Questions_answers.question_1 + "\n" + answer_01, reply_markup=keyboard)
            user_states[message.chat.id] = WAITING_FOR_QUESTION_1
        else:
            bot.send_message(message.chat.id, "Вам нужно ввести 'да' или 'нет'")
    except Exception as e:
        cleaning(message)
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_ANSWER


# Первый вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_1)
def question_01(message):
    """Здесь бот ожидает ответа на первый вопрос.

    После ввода значения от пользователя идёт проверка ответа в статическом методе convert_01 класса Currencychecking.
    Если такого варианта не существует, то к переменной error присваивается исклоючение Keyisnotexist. В таком случае
    бот отправляет соответствующее сообщение и ждёт корректного ответа от пользователя.
    Если же всё верно, то ответ пользователя добавляется в список user_answers. А затем высвечивается второй вопрос с ответами и клавиатурой для ввода.
    """

    try:
        key, error = checking.Currencychecking.convert_01(message)
        if type(error) == checking.Keyisnotexist:
            raise checking.Keyisnotexist
    except checking.Keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    except Exception as e:
        if len(result[message.chat.id]) > 0:
            for i in result[message.chat.id]:
                result[message.chat.id].pop()
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_QUESTION_1
    else:
        user_answers[message.chat.id].append(key)
        answer_02 = checking.Checking.get_value(config.Questions_answers.answers_2)
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('a'), telebot.types.KeyboardButton('b'),
                     telebot.types.KeyboardButton('c'))
        bot.send_message(message.chat.id, config.Questions_answers.question_2 + "\n" + answer_02, reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_2

# Второй вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_2)
def question_02(message):
    """Здесь бот ожидает ответа на второй вопрос.

      После ввода значения от пользователя идёт проверка ответа в статическом методе convert_02 класса Currencychecking.
      Если такого варианта не существует, то к переменной error присваивается исклоючение Keyisnotexist. В таком случае
      бот отправляет соответствующее сообщение и ждёт корректного ответа от пользователя.
      Если же всё верно, то ответ пользователя добавляется в список user_answers. А затем высвечивается третий вопрос с ответами и клавиатурой для ввода.
    """

    try:
        key, error = checking.Currencychecking.convert_02(message)
        if type(error) == checking.Keyisnotexist:
            raise checking.Keyisnotexist
    except checking.Keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    except Exception as e:
        if len(result[message.chat.id]) == 2:
            result[message.chat.id].pop()
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_QUESTION_2
    else:
        user_answers[message.chat.id].append(key)
        answer_03 = checking.Checking.get_value(config.Questions_answers.answers_3)
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('a'), telebot.types.KeyboardButton('b'),
                     telebot.types.KeyboardButton('c'), telebot.types.KeyboardButton('d'),
                     telebot.types.KeyboardButton('e'))
        bot.send_message(message.chat.id, config.Questions_answers.question_3 + "\n" + answer_03, reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_3


# Третий вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_3)
def question_03(message):
    """Здесь бот ожидает ответа на третий вопрос.

        После ввода значения от пользователя идёт проверка ответа в статическом методе convert_03 класса Currencychecking.
        Если такого варианта не существует, то к переменной error присваивается исклоючение Keyisnotexist. В таком случае
        бот отправляет соответствующее сообщение и ждёт корректного ответа от пользователя.
        Если же всё верно, то ответ пользователя добавляется в список user_answers. А затем высвечивается четвёртый вопрос с ответами и клавиатурой для ввода.
    """

    try:
        key, error = checking.Currencychecking.convert_03(message)
        if type(error) == checking.Keyisnotexist:
            raise checking.Keyisnotexist
    except checking.Keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    except Exception as e:
        if len(result[message.chat.id]) == 3:
            result[message.chat.id].pop()
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_QUESTION_3
    else:
        user_answers[message.chat.id].append(key)
        answer_04 = checking.Checking.get_value(config.Questions_answers.answers_4)
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('a'), telebot.types.KeyboardButton('b'),
                             telebot.types.KeyboardButton('c'))
        bot.send_message(message.chat.id, config.Questions_answers.question_4 + "\n" + answer_04, reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_4

# Четвёртый вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_4)
def question_04(message):
    """Здесь бот ожидает ответа на четвёртый вопрос.

          После ввода значения от пользователя идёт проверка ответа в статическом методе convert_04 класса Currencychecking.
          Если такого варианта не существует, то к переменной error присваивается исклоючение Keyisnotexist. В таком случае
          бот отправляет соответствующее сообщение и ждёт корректного ответа от пользователя.
          Если же всё верно, то ответ пользователя добавляется в список user_answers.
          Затем пользователю высвечивается результат, возможность поделиться результатом в социальных сетях, информация об опеке и т.д.
          Далее бот предлагает оставить отзыв и состояние пользователя в словаре user_states меняется на WAITING_FOR_COMMENTARY.
    """

    try:
        key, error = checking.Currencychecking.convert_04(message)
        if type(error) == checking.Keyisnotexist:
            raise checking.Keyisnotexist
    except checking.Keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    except Exception as e:
        if len(result[message.chat.id]) == 4:
            result[message.chat.id].pop()
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_QUESTION_4
    else:
        user_states[message.chat.id] = JUST_WAITING
        user_answers[message.chat.id].append(key)
        result[message.chat.id] = checking.Currencychecking.animal(user_answers[message.chat.id])
        bot.send_message(message.chat.id, f"Поздравляем! Ваше тотемное животное - {result[message.chat.id]}")
        try:
            if result[message.chat.id] == 'Манул':
                with open('files/манул.jfif', 'rb') as f:
                    bot.send_photo(message.chat.id, f, caption="Ману́л, или палла́сов кот — хищное млекопитающее семейства кошачьих. Внешностью и размерами похож на домашнего кота, но отличается более короткими массивными туловищем и лапами, круглыми зрачками, низкими ушами, а также длинным густым мехом.")
                result_img[message.chat.id] = 'манул.jfif'
            elif result[message.chat.id] == "Капибара":
                with open('files/capybara.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption="Капиба́ра, или водосви́нка, — полуводное травоядное млекопитающее из подсемейства водосвинковых, один из двух ныне существующих видов рода водосвинки. Капибара — самый крупный среди современных грызунов.")
                result_img[message.chat.id] = 'capybara.jpg'
            elif result[message.chat.id] == "Большой тукан":
                with open('files/Тукан.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption="Большо́й тука́н, или перцеяд токо — вид птиц из семейства тукановых. Крупнейший и наиболее известный представитель семейства. Распространён в большой части Южной Америки.")
                result_img[message.chat.id] = 'Тукан.jpg'
            elif result[message.chat.id] == "Сине-жёлтый ара":
                with open('files/Ара.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption="Сине-жёлтый ара — птица семейства попугаевых.")
                result_img[message.chat.id]= 'Ара.jpg'
            elif result[message.chat.id] == "Степной орёл":
                with open('files/Орел.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption="Степной орёл — хищная птица из семейства ястребиных. Согласно последним научным данным и анализам ДНК, в Африке и Индии постоянно обитает другой, внешне похожий на степного орла, вид — каменный орёл. Ранее эти виды таксономически не разделялись некоторыми учёными.")
                result_img[message.chat.id] = 'Орел.jpg'
            elif result[message.chat.id] == "Выдра":
                with open('files/выдра.jpg', 'rb') as f:
                    bot.send_photo(message.chat.id, f,
                                   caption="Вы́дра, также речная выдра, обыкновенная выдра, или поре́шня/поре́чня/поре́чь/поре́шна/поре́чна — вид хищных млекопитающих из семейства куньих, ведущих полуводный образ жизни. В литературе под словом «выдра» обычно подразумевается этот вид, хотя род выдр насчитывает несколько видов.")
                result_img[message.chat.id] = 'выдра.jpg'
            elif result[message.chat.id] == "Камышовый кот":
                with open('files/кот.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption="Камышовый кот, или хаус, или камышовая кошка, или болотная рысь — хищное млекопитающее из семейства кошачьих. Занесён в Приложение 2 CITES и Красную книгу России, как редкий и охраняемый вид. Камышовый кот крупнее любого из представителей домашних кошек: в длину достигает 60—90 см, масса от 8 до 12 кг.")
                result_img[message.chat.id] = 'кот.jpg'
        except IOError as e:
            py_logger.error(f"Ошибка при открытии файла {e}")
            bot.send_message(message.chat.id,
                             f"Ошибка при открытии файла {e}.\nПопробуйте пройти тест ещё раз!\n/startquiz")
            print(f"Ошибка при открытии файла {e}")
            cleaning(message)
            user_states[message.chat.id] = WAITING_FOR_START
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Перейти на сайт', url='https://moscowzoo.ru/my-zoo/become-a-guardian/'))
            bot.send_message(message.chat.id, ENDING_RESULT, parse_mode='html', reply_markup=markup)

            bot.send_message(message.chat.id,
                             f"Поделиться результатом в X (Twitter): https://twitter.com/intent/tweet?text=Моё тотемное животное - {result[message.chat.id]}. Узнайте своё тотемное животное с помощью телеграм-бота https://t.me/Moscow_zoo_botbotbotbot\nПоделиться результатом в VK: https://vk.com/share.php?url=Моё тотемное животное - {result[message.chat.id]}. Узнайте своё тотемное животное с помощью телеграм-бота https://t.me/Moscow_zoo_botbotbotbot\n"
                             f"Поделиться результатом в Facebook: https://www.facebook.com/sharer/sharer.php?u=Моё тотемное животное - {result[message.chat.id]}. Узнайте своё тотемное животное с помощью телеграм-бота https://t.me/Moscow_zoo_botbotbotbot",
                             disable_web_page_preview=True)

            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton('да'), telebot.types.KeyboardButton('В другой раз'),
                         telebot.types.KeyboardButton('я хочу обновить результаты'))
            bot.send_message(message.chat.id, "Желаете оставить отзыв?", reply_markup=keyboard)
            user_states[message.chat.id] = WAITING_FOR_COMMENTARY



# Ожидание комментирования
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_COMMENTARY)
def commentary(message):
    """Здесь бот ожидает ответа пользователя по поводу комментария.

    Если пользователь выбирает 'да', то бот предлагает отправить ему персональные данные.
    Состояние пользователя в словаре user_states меняется на WAITING_FOR_COMMENTARY.
    Если пользователь выбирает 'В другой раз', то бот предлагает попробовать пройти тест ещё раз.
    Состояние пользователя в словаре user_states меняется на WAITING_FOR_TRY.
    """

    try:
        if message.text.lower() == 'да':
            user_states[message.chat.id] = WAITING_FOR_PERSONAL_DATA
            bot.send_message(message.chat.id, 'Заполните ваши контактные данные ниже в формате <Ваше имя> <Ваша фамилия> <Возраст (укажите просто число)> <Город проживания> <email> через пробел')
        elif message.text == 'В другой раз':
            cleaning(message)
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
            bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
            user_states[message.chat.id] = WAITING_FOR_TRY
        elif message.text == 'я хочу обновить результаты':
            try:
                with sqlite3.connect('commets_db.SQLite') as conn:
                    cur = conn.cursor()
                    select_from_result = """SELECT *
                    FROM PERSONAL_DATA 
                    WHERE message_chat_id = ?
                    """
                    cur.execute(select_from_result, [message.chat.id])
                    data = cur.fetchone()
                if data is None:
                    raise checking.Emptydata
            except checking.Emptydata:
                bot.send_message(message.chat.id, f"Вы ещё не оставляли персональные данные и комментарий!")
                keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                keyboard.add(telebot.types.KeyboardButton('да'), telebot.types.KeyboardButton('В другой раз'))
                bot.send_message(message.chat.id, "Желаете их оставить?", reply_markup=keyboard)
                user_states[message.chat.id] = WAITING_FOR_COMMENTARY
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
                py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
                user_states[message.chat.id] = WAITING_FOR_COMMENTARY
            except sqlite3.Error as e:
                bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
                py_logger.error(f"Произошла ошибка во время выполнения запроса:{e}!")
                print(f"Произошла ошибка во время выполнения запроса:{e}!")
            else:
                get_access = access(message.chat.id)
                if get_access == False:
                    cleaning(message)
                    bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы изменить/внести результаты теста!\nДля входа в аккаунт введите команду /enter")
                    user_states[message.chat.id] = WAITING_FOR_START
                elif get_access == True:
                    try:
                        with sqlite3.connect('commets_db.SQLite') as conn:
                            cur = conn.cursor()
                            select_from_result = """SELECT *
                                           FROM RESULTS 
                                           WHERE message_chat_id = ?
                                           """
                            cur.execute(select_from_result, [message.chat.id])
                            data = cur.fetchone()
                        if data is None:
                            raise checking.Emptydata
                    except checking.Emptydata:
                        bot.send_message(message.chat.id, f"У Вас отсутствуют данные с результатами теста!")
                        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        keyboard.add(telebot.types.KeyboardButton('да'), telebot.types.KeyboardButton('нет'))
                        bot.send_message(message.chat.id, 'Хотите внести эти результаты в БД?', reply_markup=keyboard)
                        user_states[message.chat.id] = WAIT_RESULT
                    except sqlite3.Error as e:
                        bot.send_message(message.chat.id,
                                         f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
                        py_logger.error(f"Произошла ошибка во время выполнения запроса:{e}!")
                        print(f"Произошла ошибка во время выполнения запроса:{e}!")
                    else:
                        try:
                            with sqlite3.connect('commets_db.SQLite') as conn:
                                with open(f'files/{result_img[message.chat.id]}', 'rb') as f:
                                    img = f.read()
                                binary = sqlite3.Binary(img)
                                cur = conn.cursor()
                                update_query = """
                                    UPDATE RESULTS
                                    SET answer_01 = ?, answer_02 = ?, answer_03 = ?, answer_04 = ?,
                                    result = ?, animal = ?
                                    WHERE message_chat_id = ?
                                """

                                # Передача значений в виде кортежа в execute
                                cur.execute(update_query, (
                                    user_answers[message.chat.id][0], user_answers[message.chat.id][1], user_answers[message.chat.id][2], user_answers[message.chat.id][3],
                                    result[message.chat.id], binary, message.chat.id))
                        except sqlite3.Error as e:
                            bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
                            py_logger.error(f"Произошла ошибка во время выполнения запроса:{e}!")
                            print(f"Произошла ошибка во время выполнения запроса:{e}!")
                        except Exception as e:
                            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
                            py_logger.error(f"Ошибка со стороны сервера: {e}")
                            user_states[message.chat.id] = WAITING_FOR_COMMENTARY
                        else:
                            bot.send_message(message.chat.id, "Данные обновлены успешно!")
                            cleaning(message)
                            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
                            bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
                            user_states[message.chat.id] = WAITING_FOR_TRY

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_COMMENTARY


@bot.message_handler(func = lambda message: user_states.get(message.chat.id) == WAIT_RESULT)
def waiting_result(message):
    if message.text.lower() == 'да':
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                with open(f'files/{result_img[message.chat.id]}', 'rb') as f:
                    img = f.read()
                binary = sqlite3.Binary(img)
                cur = conn.cursor()
                insert_pd = '''INSERT INTO RESULTS (message_chat_id, answer_01, answer_02, answer_03, answer_04, result, animal)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                '''
                cur.execute(insert_pd,
                            [message.chat.id, user_answers[message.chat.id][0], user_answers[message.chat.id][1], user_answers[message.chat.id][2], user_answers[message.chat.id][3],
                             result[message.chat.id], binary])
        except sqlite3.Error as e:
            py_logger.error(f"Произошла ошибка при выполнении запроса {insert_pd}: {e}")
            print(f"Произошла ошибка при выполнении запроса {insert_pd}: {e}")
            bot.send_message(message.chat.id, f"Произошла ошибка при выполнении запроса {insert_pd}: {e}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(f"Ошибка со стороны сервера: {e}")
        else:
            cleaning(message)
            bot.send_message(message.chat.id, "Ваши данные успешно внесены!")
            py_logger.info('Успешное добавление данных в таблицу RESULTS')
            user_states[message.chat.id] = WAITING_FOR_TRY
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
            bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
    elif message.text.lower() == 'нет':
        cleaning(message)
        user_states[message.chat.id] = WAITING_FOR_TRY
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
        bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)


# Внесение персональных данных в БД
@bot.message_handler(func = lambda message: user_states.get(message.chat.id) == WAITING_FOR_PERSONAL_DATA)
def personal_data(message):
    """Здесь бот проверяет корректность введённых пользователем данных.

    В случае, если предоставлено больше или меньше данных, то к переменной error присваивается исключение Counterror.
    В случае, если вместо возраста введено НЕ число, то к переменной error присваивается исключение ValueError.
    В случае, если неверно введён email, то к переменной error присваивается исключение Emailerror.
    В случае, если всё хорошо, то происходит подключение к БД 'commets_db.SQLite' и происходит заполнение данными таблицы PERSONAL_DATA.

    Если же не происходит никаких ошибок, то данные заносятся в таблицу PERSONAL_DATA, а cостояние пользователя в словаре user_states меняется на COMMENT.
    Если же пользователь оставлял комментарий, то ему высвечивается соответсвующее сообщение, а cостояние в словаре user_states меняется на WAITING_FOR_TRY.
    Если же происходит какая-либо другая ошибка, то пользователю будет отправлено сообщение об этой ошибке.
    """

    try:
        message_text = message.text.split(' ')
        error = checking.Currencychecking.check_personal_data(message_text)
        if type(error) == checking.Counterror:
            raise checking.Counterror
        elif type(error) == ValueError:
            raise ValueError
        elif type(error) == checking.Emailerror:
            raise checking.Emailerror
        else:
            try:
                # Подключение к базе данных внутри функции
                with sqlite3.connect('commets_db.SQLite') as conn:
                    cursor = conn.cursor()
                    # SQL-запрос для добавления данных в таблицу PERSONAL_DATA
                    insert_pd_query = '''
                                INSERT INTO PERSONAL_DATA (name, surname, age, city, message_chat_id, email)
                                VALUES (?, ?, ?, ?, ?, ?)
                           '''

                    # Выполнение запроса для PD
                    cursor.execute(insert_pd_query, [message_text[0],message_text[1],message_text[2],message_text[3], message.chat.id, message_text[4]])

            except sqlite3.Error as e:
                py_logger.error(f'Произошла ошибка при добавлении персональных данных в базу данных (таблица PERSONAL_DATA): {e}')
                print(f'Произошла ошибка при добавлении персональных данных в базу данных (таблица PERSONAL_DATA): {e}')
                if 'UNIQUE constraint failed: PERSONAL_DATA.message_chat_id' in str(e):
                    bot.send_message(message.chat.id, 'Вы уже оставляли комментарий!')
                    try:
                        with sqlite3.connect('commets_db.SQLite') as conn:

                            cursor = conn.cursor()

                            select_com = '''
                                SELECT comment
                                FROM COMMENTS
                                WHERE message_chat_id = ?
                                '''

                            cursor.execute(select_com, [message.chat.id])
                            previous_comment = cursor.fetchone()[0]
                    except sqlite3.Error as e:
                        py_logger.error(f"Произошла ошибка во время выполнения запроса {select_com}: {e}")
                        print(f"Произошла ошибка во время выполнения запроса {select_com}: {e}")
                        bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса {select_com}: {e}. Попробуйте ещё раз!")
                    else:
                        py_logger.info(f"Запрос {select_com} прошёл успешно!")


                    bot.send_message(message.chat.id, f'Ваш комментарий: {previous_comment}')

                    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'),telebot.types.KeyboardButton('В другой раз'))
                    bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
                    user_states[message.chat.id] = WAITING_FOR_TRY
                    cleaning(message)
                else:
                    bot.send_message(message.chat.id, f'Произошла ошибка при добавлении персональных данных в базу данных: {e}\nПопробуйте ещё раз.')
                    user_states[message.chat.id] = WAITING_FOR_PERSONAL_DATA
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
                py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
                user_states[message.chat.id] = WAITING_FOR_PERSONAL_DATA
            else:
                py_logger.info('Успешное добавление данных в таблицу PERSONAL_DATA')
                try:
                    with sqlite3.connect('commets_db.SQLite') as conn:
                        with open(f'files/{result_img[message.chat.id][0]}', 'rb') as f:
                            img = f.read()
                        binary = sqlite3.Binary(img)
                        cur = conn.cursor()
                        insert_pd = '''INSERT INTO RESULTS (message_chat_id, answer_01, answer_02, answer_03, answer_04, result, animal)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                        '''
                        cur.execute(insert_pd, [message.chat.id, user_answers[message.chat.id][0], user_answers[message.chat.id][1],user_answers[message.chat.id][2],user_answers[message.chat.id][3],result[message.chat.id], binary])
                except sqlite3.Error as e:
                    py_logger.error(f"Произошла ошибка при выполнении запроса {insert_pd}: {e}")
                    print(f"Произошла ошибка при выполнении запроса {insert_pd}: {e}")
                    bot.send_message(message.chat.id, f"Произошла ошибка при выполнении запроса {insert_pd}: {e}\nПопробуйте ещё раз.")
                else:
                    bot.send_message(message.chat.id, "Придумайте логин и пароль для Вашего аккаунта.\nОни будут использоватсья для входа в Ваш аккаунт")
                    bot.send_message(message.chat.id, "Введите логин")
                    user_states[message.chat.id] = WAIT_USERNAME
                    py_logger.info('Успешное добавление данных в таблицу RESULTS')

    except checking.Counterror:
        bot.send_message(message.chat.id, 'Ошибка! Заполните ваши контактные данные ниже в формате <Имя> <Фамилия> <Возраст (укажите просто число)> <Город проживания>  <email> через пробел')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! В поле возрасте должно быть число!')
    except checking.Emailerror:
        bot.send_message(message.chat.id, "Ошибка! Неверный формат email")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
        print(f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_PERSONAL_DATA


# Проверка корректности имени пользователя
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAIT_USERNAME)
def username_01(message):
    error = checking.Currencychecking.check_username(message.text)
    if type(error) == checking.Smallusername:
        bot.send_message(message.chat.id, "Логин должен содержать не менее 10 символов")
    elif type(error) == checking.Largeusername:
        bot.send_message(message.chat.id,"Логин должен содержать не более 30 символов")
    elif type(error) == checking.Specialsymbols:
        bot.send_message(message.chat.id, 'Логин не должен сдержать специальные символы: "%@#$&*+—/|\~^=-"')
    else:
        username[message.chat.id] = message.text
        user_states[message.chat.id] = WAIT_PASSWORD
        bot.send_message(message.chat.id, "Придумайте пароль")


# Проверка корректности пароля
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAIT_PASSWORD)
def password_01(message):
    error = checking.Currencychecking.check_password(message.text)
    if type(error) == checking.Smallpassword:
        bot.send_message(message.chat.id, "Пароль должен содержать не менее 10 символов")
    elif type(error) == checking.Largepassword:
        bot.send_message(message.chat.id, "Пароль должен содержать не более 20 символов")
    elif type(error) == checking.Specialsymbols:
        bot.send_message(message.chat.id, 'Пароль не должен сдержать специальные символы: "%@#$&*+—/|\~^=-"')
    else:
        password[message.chat.id] = message.text
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                sql_ins_pas = """INSERT INTO PASSWORDS (message_chat_id, username, password)
                VALUES (?,?,?)
                """
                cur.execute(sql_ins_pas, [message.chat.id, username[message.chat.id], password[message.chat.id]])
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                sql_ins_pas = """INSERT INTO ACCESS (message_chat_id, username, password)
                VALUES (?,?,?)
                """
                cur.execute(sql_ins_pas, [message.chat.id, username[message.chat.id], password[message.chat.id]])
        except sqlite3.Error as e:
            py_logger.error(f"Произошла ошибка при выполнении запроса {sql_ins_pas}: {e}")
            print(f"Произошла ошибка при выполнении запроса {sql_ins_pas}: {e}")
            bot.send_message(message.chat.id, f"Произошла ошибка при выполнении запроса {sql_ins_pas}: {e}\nПопробуйте ещё раз.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
            print(f"Ошибка со стороны сервера: {e}")
            user_states[message.chat.id] = WAIT_PASSWORD
        else:
            bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")
            bot.send_message(message.chat.id, 'Напишите свой отзыв ниже')
            user_states[message.chat.id] = COMMENT
            py_logger.info('Успешное добавление данных в таблицу PASSWORDS')


# Отзыв
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == COMMENT)
def comment(message):
    """Здесь бот ожидает комментария от пользователя.

       Комментарий вместе с id будут занесены в таблицу COMMENTS.
       Если же не происходит никаких ошибок во время занесения данных, бот благодарит за отзыв и предлагает вновь пройти тест, а cостояние пользователя в словаре user_states меняется на WAITING_FOR_TRY.
       Если же происходит какая-либо ошибка, то пользователю будет отправлено сообщение об этой ошибке.
       """

    try:
        with sqlite3.connect('commets_db.SQLite') as conn:
            # Подключение к базе данных внутри функции
            cursor = conn.cursor()
            # SQL-запрос для добавления данных в таблицу COMMENTS
            insert_comments_query = '''
                            INSERT INTO COMMENTS (message_chat_id, comment)
                            VALUES (?, ?)
                        '''
            # Выполнение запроса для COMMENTS
            cursor.execute(insert_comments_query, [message.chat.id, message.text])

    except sqlite3.Error as e:
       py_logger.error(f'Произошла ошибка при добавлении комментария в базу данных (таблица COMMENTS): {e}\nПопробуйте ещё раз.')
       bot.send_message(message.chat.id, f'Произошла ошибка при добавлении комментария в базу данных: {e}')
       user_states[message.chat.id] = COMMENT
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = COMMENT
    else:
        cleaning(message)
        bot.send_message(message.chat.id, 'Спасибо за Ваш отзыв!')
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
        bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_TRY
        py_logger.info('Успешное добавление данных в таблицу COMMENTS')


# Ожидание ответа от пользователя
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_TRY)
def to_try(message):
    """Здесь ожидает от пользователя ответа по поводу повторного прохождения теста.

    В случае, если пользователь отказывается, то бот отправляет соответствующее сообщение, а cостояние пользователя в словаре user_states меняется на WAITING_FOR_START.
    В случае, если пользователь соглашается, то бот отображает первый вопрос с ответами, а cостояние пользователя в словаре user_states меняется на WAITING_FOR_QUESTION_1.
    """

    try:
        if message.text == 'В другой раз':
            bot.send_message(message.chat.id, "Как надумаете, введите команду /startquiz")
            user_states[message.chat.id] = WAITING_FOR_START
        elif message.text == 'Попробовать ещё раз':
            bot.send_message(message.chat.id, "Отлично, тогда начнём :)")
            answer_01 = checking.Checking.get_value(config.Questions_answers.answers_1)
            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton('a'), telebot.types.KeyboardButton('b'),
                         telebot.types.KeyboardButton('c'), telebot.types.KeyboardButton('d'),
                         telebot.types.KeyboardButton('e'), telebot.types.KeyboardButton('f'))
            bot.send_message(message.chat.id, config.Questions_answers.question_1 + "\n" + answer_01, reply_markup=keyboard)
            user_states[message.chat.id] = WAITING_FOR_QUESTION_1
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
        user_states[message.chat.id] = WAITING_FOR_TRY




# Реакция бота на случайный ввод
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == JUST_WAITING)
def just_wait(message):
    """Если вдруг в 4-ом вопросе пользователь ввёл букву два раза, то бот на это реагировать никак не будет"""

    pass

# Проверка входа
def access(chat_id):
    """Для начала происходит извлечение данных из БД. Если всё проходит без ошибок, то функция возвращает:

    - None, если пользователь не з
    """

    try:
        with sqlite3.connect('commets_db.SQLite') as conn:
            cur = conn.cursor()
            select_from_passwords = """SELECT is_access
            FROM ACCESS
            WHERE message_chat_id = ?
            """
            cur.execute(select_from_passwords, [chat_id])
            answer = cur.fetchone()[0]
    except sqlite3.Error as e:
        py_logger.error(f"Произошла ошибка во время запроса данных из БД: {e}")
        return e
    except Exception as e:
        py_logger.error(f"Ошибка со стороны сервера: {e}")
        return e
    else:
        if answer is None:
            return None
        elif answer == False:
            return False
        elif answer == True:
            return True

def change_access_true(chat_id):
    try:
        with sqlite3.connect('commets_db.SQLite') as conn:
            cur = conn.cursor()
            update_from_passwords = """
            UPDATE ACCESS
            SET is_access = TRUE
            WHERE message_chat_id = ?
            """
            cur.execute(update_from_passwords, [chat_id])

    except sqlite3.Error as e:
        bot.send_message(chat_id, f"Произошла ошибка во время авторизации: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Произошла ошибка во время авторизации: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
    else:
        bot.send_message(chat_id, "Вы успешно авторизовались!")

def change_access_false(chat_id):
    try:
        with sqlite3.connect('commets_db.SQLite') as conn:
            cur = conn.cursor()
            update_from_passwords = """
            UPDATE ACCESS
            SET is_access = FALSE
            WHERE message_chat_id = ?
            """
            cur.execute(update_from_passwords, [chat_id])

    except sqlite3.Error as e:
        bot.send_message(chat_id, f"Произошла ошибка во время выхода из аккаунта: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Произошла ошибка во время выхода из аккаунта: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера: {e}")
    else:
        bot.send_message(chat_id, "Вы успешно вышли из аккаунта")

# Команда comment
@bot.message_handler(commands=['comment'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def user_comment(message):
    """С помощью команды /comment пользователь может посмотреть свой оставленный комментарий."""

    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы просмотреть комментарий!\nДля входа в аккаунт введите команду /enter")
    elif get_access == True:
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cursor = conn.cursor()

                select_com = '''
                             SELECT comment
                             FROM COMMENTS
                             WHERE message_chat_id = ?
                             '''

                cursor.execute(select_com, [message.chat.id])
                previous_comment = cursor.fetchone()

            if previous_comment is None:
                raise TypeError
        except TypeError:
            bot.send_message(message.chat.id, "Вы ещё не оставляли отзыв")
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {e}\nПопробуйте ещё раз.")
            py_logger.error(f"Произошла ошибка во время запроса данных из БД (таблица COMMENTS): {e}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
        else:
            bot.send_message(message.chat.id, f"Ваш комментарий: {previous_comment[0]}")
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")

# Команда contact
@bot.message_handler(commands=['contact'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def contact(message):
    """С помощью команды /contact пользователь может связаться с сотрудником."""

    def contact_bd():
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cursor = conn.cursor()

                select_com = '''
                                       SELECT *
                                       FROM CONTACT
                                       WHERE message_chat_id = ?
                                   '''
                cursor.execute(select_com, [message.chat.id])
                previous_comment = cursor.fetchone()
        except sqlite3.Error as e:
            py_logger.error(f"Произошла ошибка во время запроса данных из БД: {e}")
            return e
        except Exception as e:
            py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
            return e
        else:
            py_logger.info(f"Запрос данных из БД {select_com} прошёл успешно!")
            return previous_comment


    def command_contact():
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cursor = conn.cursor()

                select_com = '''
                            SELECT *
                            FROM "Команда /contact"
                            WHERE message_chat_id = ?
                        '''
                cursor.execute(select_com, [message.chat.id])
                previous_comment = cursor.fetchone()
            if previous_comment is None:
                raise checking.Emptydata
        except sqlite3.Error as e:
            py_logger.error(f"Произошла ошибка во время запроса данных из БД (таблицы COMMENTS И PERSONAL_DATA): {e}")
            return e
        except Exception as e:
            py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
            return e
        except checking.Emptydata as e:
            return e
        else:
            py_logger.info("Запрос данных из представления 'Команда /contact' прошёл успешно!")
            return previous_comment

    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы связаться с сотрудником!\nДля входа в аккаунт введите команду /enter")
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")
    elif get_access == True:

        previous_comment = contact_bd()
        if type(previous_comment) == sqlite3.Error:
            bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {previous_comment}\nПопробуйте ещё раз.")
        elif type(previous_comment) == Exception:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {previous_comment}\nПопробуйте ещё раз.")
        elif previous_comment is not None:
            bot.send_message(message.chat.id, "Вы уже отправляли сообщение сотруднику, он свяжется с Вами в ближайшее время")
        else:
            previous_comment = command_contact()
            if type(previous_comment) == sqlite3.Error:
                bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {previous_comment}\nПопробуйте ещё раз.")
            elif type(previous_comment) == Exception:
                bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {previous_comment}\nПопробуйте ещё раз.")
            elif type(previous_comment) == checking.Emptydata:
                bot.send_message(message.chat.id, f"Ошибка! Результаты теста были очищены/ или он не пройден.\nПройдите тест заново: /startquiz")
            elif previous_comment is None:
                bot.send_message(message.chat.id, "Для того чтобы отправить сообщение сотруднику, нужно пройти тест, оставить отзыв и персональные данные")
            else:
                bot.send_message(message.chat.id, "Сотруднику отправлено следующее сообщение, в ближайшее время он с Вами свяжеться по указанному емейлу.")
                TEXT = f"Здравствуйте, меня зовут {previous_comment[0]} {previous_comment[1]}.\n"\
                f"Я бы хотел/а прокунсультироваться с Вами по поводу опеки.\n"\
                f"Вот результаты теста:\n"\
                f"Ответ на вопрос ({config.Questions_answers.question_1}) : {previous_comment[2]}\n"\
                f"Ответ на вопрос ({config.Questions_answers.question_2}) : {previous_comment[3]}\n"\
                f"Ответ на вопрос ({config.Questions_answers.question_3}) : {previous_comment[4]}\n"\
                f"Ответ на вопрос ({config.Questions_answers.question_4}) : {previous_comment[5]}\n"\
                f"Результат тестов показал, что моё тотемное животное {previous_comment[6]}, расскажите о нём/ней побольше.\n"\
                f"Мой комментарий относительно теста: {previous_comment[7]}.\n"\
                f"Email для обратной связи: {previous_comment[8]}."
                bot.send_message(message.chat.id, TEXT)
                bot.send_message(chat_id=724253475, text=TEXT)
                try:
                    with sqlite3.connect('commets_db.SQLite') as conn:
                        cursor = conn.cursor()

                        insert_contact = '''
                            INSERT INTO CONTACT(message_chat_id)
                            VALUES (?)
                            '''
                        cursor.execute(insert_contact, [message.chat.id])

                except sqlite3.Error as e:
                    bot.send_message(message.chat.id, f"Произошла ошибка при внесении данных в БД: {e}\nПопробуйте ещё раз.")
                    py_logger.error(f'Произошла ошибка при внесении данных в бд (таблица CONTACT): {e}')
                except Exception as e:
                    bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
                    py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
                else:
                    py_logger.info('Данные в таблицу CONTACT занесены успешно!')



# Команда /see_profile
@bot.message_handler(commands=['see_profile'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def see_profile(message):
    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы просмотреть данные!\nДля входа в аккаунт введите команду /enter")
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")
    elif get_access == True:
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                select_from_view = """SELECT *
                FROM Profile
                WHERE "ID телеграма" = ?
                """
                cur.execute(select_from_view, [message.chat.id])
                data = cur.fetchone()
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
            py_logger.error(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
            print(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
            print(f"Ошибка со стороны сервера: {e}")
        else:
            if data is None:
                bot.send_message(message.chat.id, "Вы ещё не оставляли персональные данные!")
            else:
                bot.send_message(message.chat.id, f"Имя: {data[0]}\nФамилия: {data[1]}\nВозраст: {data[2]}\nГород проживания: {data[3]}\nВаш комментарий относительно теста: {data[4]}\nВаш email: {data[5]}\nВаш ID: {data[6]}\n")


# Команда /see_results
@bot.message_handler(commands=['see_results'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def see_results(message):
    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы просмотреть результаты теста!\nДля входа в аккаунт введите команду /enter")
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")
    elif get_access == True:
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                select_from_view = """
                SELECT *
                FROM watch_results
                WHERE "ID телеграма" = ?
                """
                cur.execute(select_from_view, [message.chat.id])
                data = cur.fetchone()
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
            py_logger.error(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
            print(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
            print(f"Ошибка со стороны сервера: {e}")
        else:
            if data is None:
                bot.send_message(message.chat.id, "Вы ещё не проходили тест!")
            else:
                markup = telebot.types.InlineKeyboardMarkup()
                btn1 = telebot.types.InlineKeyboardButton('❌ Удалить данные! ❌', callback_data='delete')
                markup.row(btn1)
                btn2 = telebot.types.InlineKeyboardButton('✍️ Изменить данные! ✍️', callback_data='edit')
                markup.row(btn2)
                bot.send_message(message.chat.id, f"Ответ на первый вопрос: {data[0]}\nОтвет на второй вопрос: {data[1]}\nОтвет на третий вопрос: {data[2]}\nОтвет на четвёртый вопрос: {data[3]}\nРезультат: {data[4]}", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                delete_data = """
                DELETE 
                FROM RESULTS
                WHERE message_chat_id = ?
                """
                cur.execute(delete_data, [callback.message.chat.id])
        except sqlite3.Error as e:
            bot.send_message(callback.message.chat.id, f"Произошла ошибка во время очистки данных из БД:{e}!\nПопробуйте ещё раз!")
            py_logger.error(f"Произошла ошибка во время очистки данных из БД:{e}!")
            print(f"Произошла ошибка во время очистки данных из БД:{e}!")
        except Exception as e:
            bot.send_message(callback.message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(f"Ошибка со стороны сервера. Chat ID: {callback.message.chat.id}, Ошибка: {e}")
            print(f"Ошибка со стороны сервера: {e}")
        else:
            bot.edit_message_text("Ваши результаты успешно удалены!", callback.message.chat.id, callback.message.message_id)
            py_logger.info(f"Результаты пользователя {callback.message.chat.id} успешно удалены из БД!")
    elif callback.data == 'edit':
        bot.edit_message_text("Для изменения данных вам нужно перепройти тест /startquiz" , callback.message.chat.id, callback.message.message_id)


# Команда /delete_results
@bot.message_handler(commands=['delete_results'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def delete_results(message):
    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вам нужно войти в свой аккаунт, чтобы удалить результаты теста!\nДля входа в аккаунт введите команду /enter")
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")
    elif get_access == True:
        try:
            with sqlite3.connect('commets_db.SQLite') as conn:
                cur = conn.cursor()
                select_from_view = """
                SELECT *
                FROM watch_results
                WHERE "ID телеграма" = ?
                """
                cur.execute(select_from_view, [message.chat.id])
                data = cur.fetchone()
            if data is None:
                raise checking.Emptydata
        except checking.Emptydata:
            bot.send_message(message.chat.id, "Вы ещё не оставляли результаты")
        except sqlite3.Error as e:
            bot.send_message(message.chat.id, f"Произошла ошибка во время выполнения запроса:{e}!\nПопробуйте ещё раз!")
            py_logger.error(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
            print(f"Произошла ошибка во время выполнения запроса{select_from_view}:{e}!")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
            py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")
            print(f"Ошибка со стороны сервера: {e}")
        else:
            try:
                with sqlite3.connect('commets_db.SQLite') as conn:
                    cur = conn.cursor()
                    delete_data = """
                    DELETE 
                    FROM RESULTS
                    WHERE message_chat_id = ?
                    """
                    cur.execute(delete_data, [message.chat.id])
            except sqlite3.Error as e:
                bot.send_message(message.chat.id, f"Произошла ошибка во время очистки данных из БД:{e}!\nПопробуйте ещё раз!")
                py_logger.error(f"Произошла ошибка во время очистки данных из БД:{e}!")
                print(f"Произошла ошибка во время очистки данных из БД:{e}!")
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
                py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
                print(f"Ошибка со стороны сервера: {e}")
            else:
                bot.send_message(message.chat.id, "Ваши результаты успешно удалены!")
                py_logger.info(f"Результаты пользователя {message.chat.id} успешно удалены из БД!")

# Команда enter
@bot.message_handler(commands=['enter'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def enter(message):
    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access is True:
        bot.send_message(message.chat.id, "Вы уже вошли в аккаунт!")
    elif get_access is False:
        mes = bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(mes, enter_login)
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")

def enter_login(message):
    username[message.chat.id] = message.text
    mes = bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(mes, enter_password)

def enter_password(message):
    password[message.chat.id] = message.text
    try:
        with sqlite3.connect('commets_db.SQLite') as conn:
            cur = conn.cursor()
            select_data = """
            SELECT username, password
            FROM PASSWORDS
            WHERE message_chat_id = ?
            """
            cur.execute(select_data, [message.chat.id])
            answer = cur.fetchone()
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка во время извлечения данных из БД:{e}!\nПопробуйте ещё раз!")
        py_logger.error(f"Произошла ошибка во время извлечения данных из БД:{e}!")
        print(f"Произошла ошибка во время очистки данных из БД:{e}!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(f"Ошибка со стороны сервера. Chat ID: {message.chat.id}, Ошибка: {e}")
        print(f"Ошибка со стороны сервера: {e}")
    else:
        if username[message.chat.id] == answer[0] and password[message.chat.id] == answer[1]:
            change_access_true(message.chat.id)
        else:
            bot.send_message(message.chat.id, "Ошибка! Неверный логин или пароль! Попробуйте ещё раз!\n/enter")

@bot.message_handler(commands=['exit'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def exit(message):
    get_access = access(message.chat.id)
    if get_access is None:
        bot.send_message(message.chat.id, "Вы ещё не зарегистрировались!\nДля регистрации Вам нужно пройти тест, ввести персональные данные, придумать логин и пароль")
    elif get_access == False:
        bot.send_message(message.chat.id, "Вы уже вышли из аккаунта!")
    elif get_access == True:
        change_access_false(message.chat.id)
    elif type(get_access) == sqlite3.Error:
        bot.send_message(message.chat.id, f"Произошла ошибка во время запроса данных из БД: {get_access}\nПопробуйте ещё раз.")
    elif type(get_access) == Exception:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {get_access}\nПопробуйте ещё раз.")

# Реакция бота на стикеры
@bot.message_handler(content_types=['sticker', 'photo', 'audio', 'video'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def other_sticker(message):
    """Здесь описана реакция бота на стикеры"""

    try:
        bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEEAe1l7e0cgoe42ocVq97OBLYlRIsEbgACIQEAAqghIQYwcfuGXt_V5zQE')
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")


# Реакция бота на остальной текст
@bot.message_handler(content_types=['text'], func= lambda message: user_states.get(message.chat.id) is None or user_states.get(message.chat.id) == WAITING_FOR_START)
def other_text(message):
    """Здесь описана реакция бота на остальной текст"""

    try:
        bot.send_message(message.chat.id, "Для того, чтобы начать викторину, введите /startquiz.\nДля получения дополнительной информации введите /info")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка со стороны сервера: {e}\nПопробуйте ещё раз.")
        py_logger.error(message.chat.id, f"Ошибка со стороны сервера: {e}")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
