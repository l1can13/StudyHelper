import telebot
import pymysql.cursors
from config import host, user, password, db_name
from telebot import types


# Функция для подключения к базе данных
def connect_to_db():
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected successfully!")
        return connection
    except Exception as ex:
        print("Connection error!", ex)


token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
bot = telebot.TeleBot(token)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_after_creating_team = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)


@bot.message_handler(commands=['start'])
def start_message(message):
    item1 = types.KeyboardButton("Регистрация команды")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет " + message.from_user.username, reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Регистрация команды":
        bot.send_message(message.chat.id, "Заполните форму ниже")
        msg = bot.send_message(message.chat.id, "Введите имя команды: ")
        bot.register_next_step_handler(msg, after_name_of_team_text)  # после сообщения от юзера переходим в функцию


# Функция для вставки новой команды в базу данных
def insert_new_team(teamname, username):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql_request = "INSERT INTO `Команды` (`Название`, `Администратор`) VALUES (%s, %s)"
            cursor.execute(sql_request, (teamname, username))
            connection.commit()
    finally:
        connection.close()


def after_name_of_team_text(message):
    item1 = types.KeyboardButton("Удалить команду")
    markup_after_creating_team.add(item1)

    msg = bot.send_message(message.chat.id, "Имя вашей команды - " + message.text,
                           reply_markup=markup_after_creating_team)  # в message.text хранится то, что написал чел

    insert_new_team(message.text, message.from_user.username)

    bot.register_next_step_handler(msg, after_team_registered_text)


def after_team_registered_text(message):
    if message.text == "Удалить команду":
        msg = bot.send_message(message.chat.id, "Вы точно хотите удалить команду?", reply_markup=markup_yes_no)
        bot.register_next_step_handler(msg, after_team_delete_text)


# Функция для удаления определенной команды из базы данных
def delete_team(teamname):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql_request = "DELETE FROM `Команды` WHERE `Название` = %s"
            cursor.execute(sql_request, teamname)
            connection.commit()
    finally:
        connection.close()


def get_team_by_username(username):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql_request = "SELECT `Название` FROM `Команды` WHERE `Администратор` = %s"
            cursor.execute(sql_request, username)
            teamname = cursor.fetchone()
    finally:
        connection.close()
    return teamname


def after_team_delete_text(message):
    if message.text == "Да":
        teamname = get_team_by_username(message.from_user.username)
        bot.send_message(message.chat.id, "Удаляю вашу команду ")
        delete_team(teamname['Название'])
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Хорошо")


def add_new_team_member(message):
    pass


def delete_team_member(message):
    pass
    # появляется выбор участника, кроме самого админа


bot.infinity_polling()
