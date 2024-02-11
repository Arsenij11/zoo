import telebot
import checking
import config
from urllib.parse import quote
import sqlite3
import logging

bot = telebot.TeleBot(config.TOKEN)

# Словарь для хранения текущего состояния каждого пользователя
user_states = {}

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

# Результаты тестов
user_answers = []
result = []

# получение пользовательского логгера и установка уровня логирования
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler("bot.log", mode='a')
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
py_logger.addHandler(py_handler)

py_logger.info('Start_logging')

# Очистка результатов
def cleaning():
    for i in range(len(user_answers)):
        user_answers.pop()
    result.pop()


# Команда Info
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     "Телеграм-бот является частью проекта «Возьми животное под опеку»,"
                     "организованного Московским Зоопарком. Программа позволяет с помощью пожертвования на любую сумму внести "
                     "свой вклад в развитие зоопарка и сохранение биоразнообразия планеты.\n\n"
                     "Подробнее о программе: https://moscowzoo.ru/my-zoo/become-a-guardian/\n\n"
                     "Этот бот представляет собой бота-викторину, помогающую пользователю подобрать тотемное животное.\n\n"
                     "Тема викторины — «Какое у вас тотемное животное?». Вопросы могут быть с долей юмора, но основываются на реальных фактах и историях об обитателях зоопарка.\n"
                     "Чтобы начать викторину, введите команду /startquiz\nЕсли желаете посмотреть оставленный Вами комментарий, введите /comment")


# Команда start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте!\n"
                                      "Рады приветствовать Вас в боте-викторине, помогающему пользователю подобрать тотемное животное.\n"
                                      "Чтобы узнать подробности, введите команду /info.\n"
                                      "Если хотите начать, введите команду /startquiz.")


# Команда startquiz
@bot.message_handler(commands=['startquiz'])
def start_quiz(message):
    # Устанавливаем состояние ожидания ответа после команды /startquiz
    user_states[message.chat.id] = WAITING_FOR_ANSWER
    # Создаем клавиатуру для ответов
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Да'), telebot.types.KeyboardButton('Нет'))
    # Отправляем сообщение с вопросом и клавиатурой
    bot.send_message(message.chat.id, "Вам нужно выбрать лишь один правильный ответ в каждом вопросе.\nВы готовы?", reply_markup=keyboard)

# Ожидание ответа
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_ANSWER)
def quiz(message):
    # Обработка ответов
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, "Ясно :(\nКак передумаете, введите /startquiz")
        # Возвращаем пользователя в начальное состояние
        user_states[message.chat.id] = WAITING_FOR_START
    elif message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Отлично, тогда начнём :)")
        answer_01 = checking.checking.get_value(config.questions_answers.answers_1)
        bot.send_message(message.chat.id, config.questions_answers.question_1 + "\n" + answer_01)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_1
    else:
        bot.send_message(message.chat.id, "Вам нужно ввести 'да' или 'нет'")

# Первый вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_1)
def question_01(message):
    key, error = checking.currencychecking.convert_01(message)
    if type(error) == checking.keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    else:
        user_answers.append(key)
        answer_02 = checking.checking.get_value(config.questions_answers.answers_2)
        bot.send_message(message.chat.id, config.questions_answers.question_2 + "\n" + answer_02)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_2


# Второй вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_2)
def question_02(message):
    key, error = checking.currencychecking.convert_02(message)
    if type(error) == checking.keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    else:
        user_answers.append(key)
        answer_03 = checking.checking.get_value(config.questions_answers.answers_3)
        bot.send_message(message.chat.id, config.questions_answers.question_3 + "\n" + answer_03)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_3


# Третий вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_3)
def question_03(message):
    key, error = checking.currencychecking.convert_03(message)
    if type(error) == checking.keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    else:
        user_answers.append(key)
        answer_04 = checking.checking.get_value(config.questions_answers.answers_4)
        bot.send_message(message.chat.id, config.questions_answers.question_4 + "\n" + answer_04)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_4

# Четвёртый вопрос
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_QUESTION_4)
def question_04(message):
    key, error = checking.currencychecking.convert_04(message)
    if type(error) == checking.keyisnotexist:
        bot.send_message(message.chat.id, "Ошибка! Такого варианта ответа не существует!")
    else:
        user_answers.append(key)
        your_animal = checking.currencychecking.animal(user_answers)
        bot.send_message(message.chat.id, f"Поздравляем! Ваше тотемное животное - {your_animal}")
        result.append(your_animal)
        if your_animal == 'Манул':
            video_path = 'Dude.mp4'
            video = open(video_path, 'rb')
            bot.send_video(message.chat.id, video)
            video.close()
            bot.send_message(message.chat.id, "Ману́л, или палла́сов кот — хищное млекопитающее семейства кошачьих. Внешностью и размерами похож на домашнего кота, но отличается более короткими массивными туловищем и лапами, круглыми зрачками, низкими ушами, а также длинным густым мехом.")
        elif your_animal == "Капибара":
            path = 'capybara.jpg'
            f = open(path, 'rb')
            bot.send_photo(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Капиба́ра, или водосви́нка, — полуводное травоядное млекопитающее из подсемейства водосвинковых, один из двух ныне существующих видов рода водосвинки. Капибара — самый крупный среди современных грызунов.")
        elif your_animal == "Большой тукан":
            path = 'Тукан.jpg'
            f = open(path, 'rb')
            bot.send_photo(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Большо́й тука́н, или перцеяд токо — вид птиц из семейства тукановых. Крупнейший и наиболее известный представитель семейства. Распространён в большой части Южной Америки.")
        elif your_animal == "Сине-жёлтый ара":
            path = 'Ара.jpg'
            f = open(path, 'rb')
            bot.send_photo(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Сине-жёлтый ара — птица семейства попугаевых.")
        elif your_animal == "Степной орёл":
            path = 'Орел.jpg'
            f = open(path, 'rb')
            bot.send_photo(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Степной орёл — хищная птица из семейства ястребиных. Согласно последним научным данным и анализам ДНК, в Африке и Индии постоянно обитает другой, внешне похожий на степного орла, вид — каменный орёл. Ранее эти виды таксономически не разделялись некоторыми учёными.")
        elif your_animal == "Выдра":
            path = 'Выдра.MP4'
            f = open(path, 'rb')
            bot.send_video(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Вы́дра, также речная выдра, обыкновенная выдра, или поре́шня/поре́чня/поре́чь/поре́шна/поре́чна — вид хищных млекопитающих из семейства куньих, ведущих полуводный образ жизни. В литературе под словом «выдра» обычно подразумевается этот вид, хотя род выдр насчитывает несколько видов.")
        elif your_animal == "Камышовый кот":
            path = 'кот.jpg'
            f = open(path, 'rb')
            bot.send_photo(message.chat.id, f)
            f.close()
            bot.send_message(message.chat.id, "Камышовый кот, или хаус, или камышовая кошка, или болотная рысь — хищное млекопитающее из семейства кошачьих. Занесён в Приложение 2 CITES и Красную книгу России, как редкий и охраняемый вид. Камышовый кот крупнее любого из представителей домашних кошек: в длину достигает 60—90 см, масса от 8 до 12 кг.")

        bot.send_message(message.chat.id, "«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих зоопарку заботиться о его обитателях. "
                "Программа позволяет с помощью пожертвования на любую сумму внести свой вклад в развитие зоопарка и сохранение биоразнообразия планеты.\n"

"Сейчас в Московском зоопарке живёт около 6 000 животных, представляющих примерно 1 100 биологических видов мировой фауны. "
"Каждое животное уникально, и все требуют внимание и уход. Из ежедневного рациона питания животного как раз и рассчитывается стоимость его опеки.\n"

"Взять под опеку можно разных обитателей зоопарка, например, слона, льва, суриката или фламинго. "
"Это возможность помочь любимому животному или даже реализовать детскую мечту подружиться с настоящим диким зверем. "
            "Почётный статус опекуна позволяет круглый год навещать подопечного, быть в курсе событий его жизни и самочувствия.\n"

"Участником программы может стать любой неравнодушный: и ребёнок, и большая корпорация. "
"Поддержка опекунов помогает зоопарку улучшать условия для животных и повышать уровень их благополучия.\n"
"Всего существуют 5 уровней участия в программе:\n"
 "1. Индивидуальный (пожертвование до 50 тыс. рублей в год)\n"
 "2. Партнерский (пожертвование от 50 до 150 тыс. рублей в год)\n"
 "3. Представительский (пожертвование от 150 до 300 тыс. рублей в год)\n"
 "4. Почетный (пожертвование от 300 тыс. до 1 млн. рублей в год)\n"
 "5. Президентский (пожертвование от 1 млн. рублей в год и более)\nБолее подробно: https://moscowzoo.ru/my-zoo/become-a-guardian/")


        result_message = f"Моё тотемное животное - {your_animal}. Узнай своё тотемное животное с помощью телеграм-бота https://t.me/Moscow_zoo_botbotbotbot"


        bot.send_message(message.chat.id, f"Поделиться результатом в X (Twitter): https://twitter.com/intent/tweet?text={quote(result_message)}\nПоделиться результатом в VK: https://vk.com/share.php?url={quote(result_message)}\n"
                                          f"Поделиться результатом в Facebook: https://www.facebook.com/sharer/sharer.php?u={quote(result_message)}", disable_web_page_preview=True)

        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('да'), telebot.types.KeyboardButton('В другой раз'))
        bot.send_message(message.chat.id, "Желаете оставить отзыв?", reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_COMMENTARY

# Ожидание комментирования
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_COMMENTARY)
def commentary(message):
    if message.text.lower() == 'да':
        user_states[message.chat.id] = WAITING_FOR_PERSONAL_DATA
        bot.send_message(message.chat.id, 'Заполните ваши контактные данные ниже в формате <Имя> <Фамилия> <Возраст (укажите просто число)> <Город проживания> <email> через пробел')
    elif message.text == 'В другой раз':
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
        bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_TRY
        cleaning()

# Внесение персональных данных в БД
@bot.message_handler(func = lambda message: user_states.get(message.chat.id) == WAITING_FOR_PERSONAL_DATA)
def personal_data(message):
    message_text = message.text.split(' ')
    error = checking.currencychecking.check_personal_data(message_text)
    if type(error) == checking.counterror:
        bot.send_message(message.chat.id, 'Ошибка! Заполните ваши контактные данные ниже в формате <Имя> <Фамилия> <Возраст (укажите просто число)> <Город проживания>  <email> через пробел')
    elif type(error) == ValueError:
        bot.send_message(message.chat.id, 'Ошибка! В поле возрасте должно быть число!')
    elif type(error) == checking.emailerror:
        bot.send_message(message.chat.id ,"Ошибка! Неверный формат email")
    else:
        # Подключение к базе данных внутри функции
        conn = sqlite3.connect('commets_db.SQLite')
        cursor = conn.cursor()
        # SQL-запрос для добавления данных в таблицу PERSONAL_DATA
        insert_pd_query = '''
                    INSERT INTO PERSONAL_DATA (name, surname, age, city, message_chat_id, answer_01, answer_02, answer_03, answer_04, result, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               '''
        try:
            # Выполнение запроса для PD
            cursor.execute(insert_pd_query, [message_text[0],message_text[1],message_text[2],message_text[3], message.chat.id, user_answers[0], user_answers[1], user_answers[2], user_answers[3], result[0], message_text[4]])
            conn.commit()
        except sqlite3.Error as e:
            py_logger.info(f'Произошла ошибка при добавлении комментария в базу данных (таблица PERSONAL_DATA): {e}')
            if 'UNIQUE constraint failed: PERSONAL_DATA.message_chat_id' in str(e):
                bot.send_message(message.chat.id, 'Вы уже оставляли комментарий!')

                conn.close()

                conn = sqlite3.connect('commets_db.SQLite')
                cursor = conn.cursor()

                select_com = '''
                    SELECT comment
                    FROM COMMENTS
                    WHERE message_chat_id = ?
                    '''

                cursor.execute(select_com, [message.chat.id])
                previous_comment = cursor.fetchone()
                conn.close()

                bot.send_message(message.chat.id, f'Ваш комментарий: {previous_comment[0]}')

                keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'),telebot.types.KeyboardButton('В другой раз'))
                bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
                user_states[message.chat.id] = WAITING_FOR_TRY
                cleaning()

        else:
            bot.send_message(message.chat.id, 'Напишите свой отзыв ниже')
            user_states[message.chat.id] = COMMENT
            conn.close()
            py_logger.info('Успешное добавление данных в таблицу PERSONAL_DATA')


# Отзыв
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == COMMENT)
def comment(message):
    # Подключение к базе данных внутри функции
    conn = sqlite3.connect('commets_db.SQLite')
    cursor = conn.cursor()
    # SQL-запрос для добавления данных в таблицу COMMENTS
    insert_comments_query = '''
                  INSERT INTO COMMENTS (message_chat_id, comment)
                  VALUES (?, ?)
              '''
    try:
        # Выполнение запроса для COMMENTS
        cursor.execute(insert_comments_query, [message.chat.id, message.text])
        conn.commit()
    except sqlite3.Error as e:
       py_logger.info(f'Произошла ошибка при добавлении комментария в базу данных (таблица COMMENTS): {e}')
    else:
        bot.send_message(message.chat.id, 'Спасибо за Ваш отзыв!')
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton('Попробовать ещё раз'), telebot.types.KeyboardButton('В другой раз'))
        bot.send_message(message.chat.id, "Не желаете пройти тест ещё раз?", reply_markup=keyboard)
        user_states[message.chat.id] = WAITING_FOR_TRY
        cleaning()
        py_logger.info('Успешное добавление данных в таблицу COMMENTS')
    finally:
        # Закрытие соединения с базой данных
        conn.close()


# Ожидание ответа от пользователя
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == WAITING_FOR_TRY)
def to_try(message):
    if message.text == 'В другой раз':
        bot.send_message(message.chat.id, "Как надумаете, введите команду /startquiz")
        user_states[message.chat.id] = WAITING_FOR_START
    elif message.text == 'Попробовать ещё раз':
        bot.send_message(message.chat.id, "Отлично, тогда начнём :)")
        answer_01 = checking.checking.get_value(config.questions_answers.answers_1)
        bot.send_message(message.chat.id, config.questions_answers.question_1 + "\n" + answer_01)
        user_states[message.chat.id] = WAITING_FOR_QUESTION_1

# Команда comment
@bot.message_handler(commands=['comment'])
def user_comment(message):
    try:
        conn = sqlite3.connect('commets_db.SQLite')
        cursor = conn.cursor()

        select_com = '''
                     SELECT comment
                     FROM COMMENTS
                     WHERE message_chat_id = ?
                     '''

        cursor.execute(select_com, [message.chat.id])
        previous_comment = cursor.fetchone()
        conn.close()
        if type(previous_comment[0]) == TypeError:
            raise TypeError
    except TypeError:
        bot.send_message(message.chat.id, "Вы ещё не оставляли отзыв")
    else:
        bot.send_message(message.chat.id, f"Ваш комментарий: {previous_comment[0]}")

# Команда contact
@bot.message_handler(commands=['contact'])
def contact(message):
    try:
        conn = sqlite3.connect('commets_db.SQLite')
        cursor = conn.cursor()

        select_com = '''
            SELECT c.comment, pd.name, pd.surname, pd.answer_01, pd.answer_02, pd.answer_03, pd.answer_04, pd.result, pd.email
            FROM COMMENTS c
            join PERSONAL_DATA pd ON pd.message_chat_id = c.message_chat_id 
            WHERE pd.message_chat_id = ?
        '''
        cursor.execute(select_com, [message.chat.id])
        previous_comment = cursor.fetchone()
        conn.close()
        if type(previous_comment[0]) == TypeError:
            raise TypeError
    except TypeError:
        bot.send_message(message.chat.id, "Для того чтобы отправить сообщение сотруднику, нужно пройти тест, оставить отзыв и персональные данные")
    else:
        conn = sqlite3.connect('commets_db.SQLite')
        cursor = conn.cursor()

        select_com = '''
                    SELECT *
                    FROM CONTACT 
                    WHERE message_chat_id = ?
                '''
        cursor.execute(select_com, [message.chat.id])
        previous_comment = cursor.fetchone()
        conn.close()
        if previous_comment == None:
            conn = sqlite3.connect('commets_db.SQLite')
            cursor = conn.cursor()

            select_com = '''
                       SELECT c.comment, pd.name, pd.surname, pd.answer_01, pd.answer_02, pd.answer_03, pd.answer_04, pd.result, pd.email
                       FROM COMMENTS c
                       join PERSONAL_DATA pd ON pd.message_chat_id = c.message_chat_id 
                       WHERE pd.message_chat_id = ?
                   '''
            cursor.execute(select_com, [message.chat.id])
            previous_comment = cursor.fetchone()
            conn.close()
            bot.send_message(message.chat.id, "Сотруднику отправлено следующее сообщение, в ближайшее время он с Вами свяжеться по указанному емейлу.")
            bot.send_message(message.chat.id, f"Здравствуйте, меня зовут {previous_comment[2]} {previous_comment[1]}.\n"
                                        f"Я бы хотел/а прокунсультироваться с Вами по поводу опеки.\n"
                                        f"Вот результаты теста:\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_1}) : {previous_comment[3]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_2}) : {previous_comment[4]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_3}) : {previous_comment[5]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_4}) : {previous_comment[6]}\n"
                                        f"Результат тестов показал, что моё тотемное животное {previous_comment[7]}, расскажите о нём/ней побольше.\n"
                                        f"Мой комментарий относительно теста: {previous_comment[0]}.\n"
                                        f"Email для обратной связи: {previous_comment[8]}.")

            bot.send_message(chat_id = 6877936532, text= f"Здравствуйте, меня зовут {previous_comment[2]} {previous_comment[1]}.\n"
                                        f"Я бы хотел/а прокунсультироваться с Вами по поводу опеки.\n"
                                        f"Вот результаты теста:\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_1}) : {previous_comment[3]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_2}) : {previous_comment[4]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_3}) : {previous_comment[5]}\n"
                                        f"Ответ на вопрос ({config.questions_answers.question_4}) : {previous_comment[6]}\n"
                                        f"Результат тестов показал, что моё тотемное животное {previous_comment[7]}, расскажите о нём/ней побольше.\n"
                                        f"Мой комментарий относительно теста: {previous_comment[0]}.\n"
                                        f"Email для обратной связи: {previous_comment[8]}.")
            try:
                conn = sqlite3.connect('commets_db.SQLite')
                cursor = conn.cursor()

                insert_contact = '''
                                  INSERT INTO CONTACT(message_chat_id)
                                  VALUES (?)
                                '''
                cursor.execute(insert_contact, [message.chat.id])
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                py_logger.info(f'Произошла ошибка при внесении данных в бд (таблица CONTACT): {e}')
            else:
                py_logger.info('Данные в таблицу CONTACT занесены успешно!')
        else:
            bot.send_message(message.chat.id, "Вы уже отправляли сообщение сотруднику. Он с Вами скоро свяжется.")

# Реакция бота на остальной текст
@bot.message_handler(content_types=['text'])
def other_text(message):
    bot.send_message(message.chat.id, "Для того, чтобы начать викторину, введите /startquiz.\nДля получения дополнительной информации введите /info")


bot.polling(none_stop=True)
