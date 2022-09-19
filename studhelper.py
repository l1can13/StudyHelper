import telebot
from telebot import types


token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
bot = telebot.TeleBot(token)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_after_creating_team = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_yes_no = types.ReplyKeyboardMarkup(resize_keyboard=True)


@bot.message_handler(commands=['start'])
def start_message(message):
    item1 = types.KeyboardButton("Регистрация команды")
    markup.add(item1)
    bot.send_message(message.chat.id, "Тест. Привет", reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Регистрация команды":
        bot.send_message(message.chat.id, "Заполните форму ниже")
        msg = bot.send_message(message.chat.id, "Введите имя команды: ")
        bot.register_next_step_handler(msg, after_name_of_team_text) # после сообщения от юзера переходим в функцию


def after_name_of_team_text(message):
    item1 = types.KeyboardButton("Удалить команду")
    markup_after_creating_team.add(item1)
    item2 = types.KeyboardButton("Добавить участника")
    markup_after_creating_team.add(item2)
    item3 = types.KeyboardButton("Удалить участника")
    markup_after_creating_team.add(item3)
    msg = bot.send_message(message.chat.id, "Имя вашей команды - " + message.text,
                     reply_markup=markup_after_creating_team) # в message.text хранится то, что написал чел
    bot.register_next_step_handler(msg, after_team_registered_text)


def after_team_registered_text(message):
    if message.text == "Удалить команду":
        msg = bot.send_message(message.chat.id, "Вы точно хотите удалить команду?", reply_markup=markup_yes_no)
        bot.register_next_step_handler(msg, after_team_delete_text)
    elif message.text == "Добавить участника":
        msg = bot.send_message(message.chat.id, "Укажите ID нового участника")
        bot.register_next_step_handler(msg, add_new_team_member)
    elif message.text == "Удалить участника":
        msg = bot.send_message(message.chat.id, "Выберите участника которого хотите удалить")
        bot.register_next_step_handler(msg, delete_team_member)

def after_team_delete_text(message):
    if message.text == "Да":
        # team = get_team_from_bd() ? находим эту команду в бд по айди админа ?
        bot.send_message(message.chat.id, "Удаляю вашу команду ")
        # delete_team_from_bd(team) ? удаляем эту команду из бд ?
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Хорошо")


def add_new_team_member(message):
    pass


def delete_team_member(message):
    pass
    # появляется выбор участника, кроме самого админа


bot.infinity_polling()


