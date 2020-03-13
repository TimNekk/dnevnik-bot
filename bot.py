import telebot
from telebot import types
import pickle
import os
import networking as nw

bot = telebot.TeleBot('983970585:AAHtqErypinRDlQ7mPlUVC_dgfZ085CAGFk')  # Установка токена бота


# ---------------------------------------------------------------
# Обработчики сообщение
# ---------------------------------------------------------------


@bot.message_handler(commands=['start'])
def send_start_message(message):
    # Если пользователь существует
    users = get_users()
    if message.chat.id in users:
        user = users[message.chat.id]

        bot.send_message(message.chat.id, message.text)

    # Если новый пользователь
    else:
        # Создание пользователся
        user = {'login': '', 'password': '', 'pages': {}}
        add_user(user, message.chat.id)  # Добавление в users.txt

        # Использовать ник или имя
        if message.from_user.first_name:
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
    # Вход по логину
    if call.data == 'login':
        bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаление предыдущего сообщения
        get_user_login(call.message)  # Получить логин от пользователя


# ---------------------------------------------------------------
# Отбработчики следующего сообщения
# ---------------------------------------------------------------


def get_user_login(message):
    # Отправка сообщения
    text = 'Введите *Логин* _(телефон, email или СНИЛС)_'
    msg = bot.send_message(message.chat.id, text, reply_markup=get_cancel_keyboard(), parse_mode='Markdown')

    bot.register_next_step_handler(msg, get_user_password)


def get_user_password(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Установка логина пользователя
    login = message.text
    user['login'] = login
    save_users(users)

    # Отправка сообщения
    text = 'Введите *Пароль*'
    msg = bot.send_message(message.chat.id, text, reply_markup=get_cancel_keyboard(), parse_mode='Markdown')

    bot.register_next_step_handler(msg, get_user_pages)


def get_user_pages(message):
    # Получить пользователя
    users = get_users()
    user = users[message.chat.id]

    # Установка пароль пользователя
    password = message.text
    user['password'] = password
    save_users(users)

    # Удаление 4 предыдущих сообщений
    for i in range(4):
        bot.delete_message(message.chat.id, message.message_id - i)

    pages = nw.get_diary_page(user['login'], user['password'])

    if pages:
        # Установка страниц пользователя
        user['pages']['timetable'] = pages[0]
        user['pages']['marks'] = pages[1]
    else:
        print('Ошибка')


# ---------------------------------------------------------------
# Клавиатуры
# ---------------------------------------------------------------


def get_cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    keyboard.add(b1)
    return keyboard


def get_keyboard_new_user():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Войти', callback_data='login')
    b2 = types.InlineKeyboardButton('Инвайт-код', callback_data='invite-code')
    keyboard.add(b1, b2)
    return keyboard


# ---------------------------------------------------------------
# Работа с пользователями
# ---------------------------------------------------------------


def save_users(users):
    with open('users.txt', 'wb') as file:
        pickle.dump(users, file)


def add_user(user, chat_id):
    with open('users.txt', 'rb') as file:
        users = pickle.load(file)

    users[chat_id] = user

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


if __name__ == '__main__':
    # Существует ли users.txt
    if os.path.getsize('users.txt') == 0:
        reset_users_file()

    reset_users_file()

    bot.skip_pending = True
    print('Bot started successfully')
    bot.polling(none_stop=True, interval=2)