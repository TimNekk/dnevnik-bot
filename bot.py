import telebot
from telebot import types
import pickle
import os
import networking as nw
import scraping as s
import datetime
import secrets

bot = telebot.TeleBot('983970585:AAHtqErypinRDlQ7mPlUVC_dgfZ085CAGFk')  # Установка токена бота


# ---------------------------------------------------------------
# Обработчики сообщение
# ---------------------------------------------------------------


@bot.message_handler(commands=['start'])
def start_message_manager(message):
    users = get_users()

    # Если пользователь существует
    if message.chat.id in users:
        user = users[message.chat.id]

        # Есть ли страницы у пользователя
        if user['pages']:
            # Отправка сообщения
            name = s.get_fio(user['pages']['timetable_now'])
            text = f'Здравствуйте, {name}\n'  # TODO - Полученеи имени и фамилии из timetable_page
            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard())
        else:
            set_user_pages(message)

    # Если новый пользователь
    else:
        print(f'Новый пользователь {message.from_user.username} - {message.chat.id}')
        # Создание пользователся
        user = create_user()
        users[message.chat.id] = user
        save_users(users)

        # Отправка сообщения
        if message.from_user.first_name:  # Использовать ник или имя
            text = f'Привет, {message.from_user.first_name}!'
        else:
            text = f'Привет, {message.from_user.username}!'
        text += '\nЯ - Дневник Бот 😄\n\nМожешь войти в свою учетную запись или ввести инвайт-код'
        bot.send_message(message.chat.id, text, reply_markup=get_keyboard_new_user())


# ---------------------------------------------------------------
# Обработчик Callback
# ---------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Войти
    if call.data == 'login':
        bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаление предыдущего сообщения
        get_user_login(call.message)  # Получить логин от пользователя

    # Инвайт-код
    elif call.data == 'invite-code':
        bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаление предыдущего сообщения
        use_invite_code(call.message)


    # Вернуться в главное меню
    elif call.data == 'main_menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаление предыдущего сообщения
        start_message_manager(call.message)  # Получить логин от пользователя

    # Расписание
    elif call.data == 'timetable':
        # Отправка сообщения
        text = 'На какой день показать расписание?'
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_timetable_keyboard())

    # Сегодня
    elif call.data == 'timetable_today':
        weekday = datetime.date.today().weekday() + 1  # Сегодня
        if weekday == 5 or weekday == 6:  # Если суббота или воскресение
            weekday = 4  # Тогда пятница
        send_timetable(call.message, weekday, 'timetable_now')

    # Завтра
    elif call.data == 'timetable_tomorrow':
        weekday = (datetime.date.today() + datetime.timedelta(days=1)).weekday()  # Завтра
        if weekday == 5 or weekday == 6:  # Если суббота или воскресение
            weekday = 0  # Тогда понедельник
            send_timetable(call.message, weekday, 'timetable_next')
        else:
            send_timetable(call.message, weekday, 'timetable_now')

    # Другой день
    elif call.data == 'timetable_weeks':
        # Отправка сообщения
        text = 'Выберите неделю'
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_weeks_keyboard())

    # Прошлая неделя
    elif call.data == 'timetable_pre':
        # Отправка сообщения
        text = 'Выберите день на прошлой неделе'
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_days_pre_keyboard())
    elif call.data == 'timetable_pre_0':
        send_timetable(call.message, 0, 'timetable_pre')
    elif call.data == 'timetable_pre_1':
        send_timetable(call.message, 1, 'timetable_pre')
    elif call.data == 'timetable_pre_2':
        send_timetable(call.message, 2, 'timetable_pre')
    elif call.data == 'timetable_pre_3':
        send_timetable(call.message, 3, 'timetable_pre')
    elif call.data == 'timetable_pre_4':
        send_timetable(call.message, 4, 'timetable_pre')
    elif call.data == 'timetable_pre_5':
        send_timetable(call.message, 5, 'timetable_pre')

    # Текущая неделя
    elif call.data == 'timetable_now':
        # Отправка сообщения
        text = 'Выберите день на текущей неделе'
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_days_now_keyboard())
    elif call.data == 'timetable_now_0':
        send_timetable(call.message, 0, 'timetable_now')
    elif call.data == 'timetable_now_1':
        send_timetable(call.message, 1, 'timetable_now')
    elif call.data == 'timetable_now_2':
        send_timetable(call.message, 2, 'timetable_now')
    elif call.data == 'timetable_now_3':
        send_timetable(call.message, 3, 'timetable_now')
    elif call.data == 'timetable_now_4':
        send_timetable(call.message, 4, 'timetable_now')
    elif call.data == 'timetable_now_5':
        send_timetable(call.message, 5, 'timetable_now')

    # След. неделя
    elif call.data == 'timetable_next':
        # Отправка сообщения
        text = 'Выберите день на след. неделе'
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=get_days_next_keyboard())
    elif call.data == 'timetable_next_0':
        send_timetable(call.message, 0, 'timetable_next')
    elif call.data == 'timetable_next_1':
        send_timetable(call.message, 1, 'timetable_next')
    elif call.data == 'timetable_next_2':
        send_timetable(call.message, 2, 'timetable_next')
    elif call.data == 'timetable_next_3':
        send_timetable(call.message, 3, 'timetable_next')
    elif call.data == 'timetable_next_4':
        send_timetable(call.message, 4, 'timetable_next')
    elif call.data == 'timetable_next_5':
        send_timetable(call.message, 5, 'timetable_next')

    # Насттройки
    elif call.data == 'settings':
        send_settings(call.message)


# ---------------------------------------------------------------
# Функции
# ---------------------------------------------------------------


def use_invite_code()



def send_settings(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    text = f'Инвайт-код: '
    if user['invite_code']:




def send_timetable(message, weekday, page_name):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Получние расписания
    lessons = s.get_timetable(user['pages'][page_name], weekday)
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']  # Квадратики с цифрами
    if lessons:
        text = ''
        for i, lesson in enumerate(lessons, 0):  # Проход через все уроки
            # Название
            text += f'*{numbers[i]} {lesson[0]}'

            # Оценки
            if lesson[2]:
                text += ' | '
                for mark in lesson[2]:
                    text += f'{mark} '
            text += '*'

            # Задание
            if lesson[1]:
                text += f'\n_{lesson[1]}_\n\n'
            else:
                text += '\n\n'
    else:
        text = 'На этот день нет расписания'

    bot.edit_message_text(text, message.chat.id, message.message_id, reply_markup=get_back_keyboard(), parse_mode='Markdown')


def get_user_login(message):
    # Отправка сообщения
    text = 'Введите *Логин* _(телефон, email или СНИЛС)_'
    msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')

    bot.register_next_step_handler(msg, process_user_login)


def process_user_login(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Установка логина пользователя
    login = message.text
    user['login'] = login
    save_users(users)

    get_user_password(message)


def get_user_password(message):
    # Отправка сообщения
    text = 'Введите *Пароль*'
    msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')

    bot.register_next_step_handler(msg, process_user_password)


def process_user_password(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Установка пароль пользователя
    password = message.text
    user['password'] = password
    save_users(users)

    set_user_pages(message)


def set_user_pages(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Удаление 4 предыдущих сообщений
    for i in range(4):
        bot.delete_message(message.chat.id, message.message_id - i)

    pages = nw.get_diary_pages(user['login'], user['password'])

    if pages:
        # Установка страниц пользователя
        user['pages']['timetable_now'] = pages[0]
        user['pages']['timetable_next'] = pages[1]
        user['pages']['timetable_pre'] = pages[2]
        user['pages']['marks'] = pages[3]
        save_users(users)
    else:
        print('Ошибка входа')
        delete_user(message)

        # Отправка сообщения
        text = '❌ *Неверные данные* ❌'
        msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')

    start_message_manager(message)


# ---------------------------------------------------------------
# Клавиатуры
# ---------------------------------------------------------------


def get_back_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='main_menu')
    keyboard.add(back_b)
    return keyboard


def get_keyboard_new_user():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Войти', callback_data='login')
    b2 = types.InlineKeyboardButton('Инвайт-код', callback_data='invite-code')
    keyboard.add(b1, b2)
    return keyboard


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Расписание', callback_data='timetable')
    b2 = types.InlineKeyboardButton('Оценки', callback_data='marks')
    b3 = types.InlineKeyboardButton('Настройки', callback_data='settings')
    keyboard.add(b1, b2)
    keyboard.add(b3)
    return keyboard


def get_timetable_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Сегодня', callback_data='timetable_today')
    b2 = types.InlineKeyboardButton('Завтра', callback_data='timetable_tomorrow')
    b3 = types.InlineKeyboardButton('Другой день', callback_data='timetable_weeks')
    keyboard.add(b1, b2, b3)

    # Кнопка назад
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='main_menu')
    keyboard.add(back_b)
    return keyboard


# def get_weeks_keyboard():
#     keyboard = types.InlineKeyboardMarkup()
#     b1 = types.InlineKeyboardButton('Прошлая неделя', callback_data='timetable_pre')
#     b2 = types.InlineKeyboardButton('Текущая неделя', callback_data='timetable_now')
#     b3 = types.InlineKeyboardButton('След. неделя', callback_data='timetable_next')
#     keyboard.add(b1)
#     keyboard.add(b2)
#     keyboard.add(b3)
#
#     # Кнопка назад
#     back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='timetable')
#     keyboard.add(back_b)
#     return keyboard

def get_weeks_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Прошлая', callback_data='timetable_pre')
    b2 = types.InlineKeyboardButton('Текущая', callback_data='timetable_now')
    b3 = types.InlineKeyboardButton('След.', callback_data='timetable_next')
    keyboard.add(b1, b2, b3)

    # Кнопка назад
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='timetable')
    keyboard.add(back_b)
    return keyboard


def get_days_pre_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Пн', callback_data='timetable_pre_0')
    b2 = types.InlineKeyboardButton('Вт', callback_data='timetable_pre_1')
    b3 = types.InlineKeyboardButton('Ср', callback_data='timetable_pre_2')
    b4 = types.InlineKeyboardButton('Чт', callback_data='timetable_pre_3')
    b5 = types.InlineKeyboardButton('Пт', callback_data='timetable_pre_4')
    b6 = types.InlineKeyboardButton('Сб', callback_data='timetable_pre_5')
    keyboard.add(b1, b2, b3)
    keyboard.add(b4, b5, b6)

    # Кнопка назад
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='timetable_weeks')
    keyboard.add(back_b)
    return keyboard


def get_days_now_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Пн', callback_data='timetable_now_0')
    b2 = types.InlineKeyboardButton('Вт', callback_data='timetable_now_1')
    b3 = types.InlineKeyboardButton('Ср', callback_data='timetable_now_2')
    b4 = types.InlineKeyboardButton('Чт', callback_data='timetable_now_3')
    b5 = types.InlineKeyboardButton('Пт', callback_data='timetable_now_4')
    b6 = types.InlineKeyboardButton('Сб', callback_data='timetable_now_5')
    keyboard.add(b1, b2, b3)
    keyboard.add(b4, b5, b6)

    # Кнопка назад
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='timetable_weeks')
    keyboard.add(back_b)
    return keyboard


def get_days_next_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Пн', callback_data='timetable_next_0')
    b2 = types.InlineKeyboardButton('Вт', callback_data='timetable_next_1')
    b3 = types.InlineKeyboardButton('Ср', callback_data='timetable_next_2')
    b4 = types.InlineKeyboardButton('Чт', callback_data='timetable_next_3')
    b5 = types.InlineKeyboardButton('Пт', callback_data='timetable_next_4')
    b6 = types.InlineKeyboardButton('Сб', callback_data='timetable_next_5')
    keyboard.add(b1, b2, b3)
    keyboard.add(b4, b5, b6)

    # Кнопка назад
    back_b = types.InlineKeyboardButton('Назад ↩️', callback_data='timetable_weeks')
    keyboard.add(back_b)
    return keyboard


# ---------------------------------------------------------------
# Работа с users.txt
# ---------------------------------------------------------------


def create_user():
    user = {'login': '', 'password': '', 'pages': {}, 'from_invite_code': False, 'invite_code': False}
    return user


def delete_user(message):
    users = get_users()
    users.pop(message.chat.id)
    save_users(users)


def save_users(users):
    with open('users.txt', 'wb') as file:
        pickle.dump(users, file)


def get_users():
    with open('users.txt', 'rb') as file:
        users = pickle.load(file)
        return users


def reset_users_file():
    with open('users.txt', 'wb') as file:
        pickle.dump({}, file)
    print('users.txt reset')


# ---------------------------------------------------------------
# Работа с инвайт-кодаами
# ---------------------------------------------------------------


def create_invite_code(user):
    invite_code = secrets.token_hex()[:7]
    invite_codes = get_invite_codes()
    invite_codes[invite_code] = {'login': user['login'], 'password': user['password']}
    save_invite_codes(invite_codes)
    return invite_code


def save_invite_codes(invite_codes):
    with open('invite_codes.txt', 'wb') as file:
        pickle.dump(invite_codes, file)


def get_invite_codes():
    with open('invite_codes.txt', 'rb') as file:
        invite_codes = pickle.load(file)
        return invite_codes


def reset_invite_codes_file():
    with open('invite_codes.txt', 'wb') as file:
        pickle.dump({}, file)
    print('invite_codes.txt reset')


if __name__ == '__main__':
    # Существует ли users.txt
    if os.path.getsize('users.txt') == 0:
        reset_users_file()

    # reset_users_file()
    # reset_invite_codes_file()

    bot.skip_pending = True
    print('Bot started successfully')
    bot.polling(none_stop=True, interval=2)