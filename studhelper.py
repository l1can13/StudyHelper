import telebot
from telebot import types


token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
bot = telebot.TeleBot(token)
str_for_item1 = "Регистрация команды"
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

@bot.message_handler(commands=['start'])
def start_message(message):
    item1 = types.KeyboardButton(str_for_item1)
    markup.add(item1)
    bot.send_message(message.chat.id, "Тест. Привет", reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == str_for_item1:
        bot.send_message(message.chat.id, "Заполните форму ниже")
        msg = bot.send_message(message.chat.id, "Введите имя команды: ")
        bot.register_next_step_handler(msg, after_name_of_command_text) # после сообщения от юзера переходим в функцию




def after_name_of_command_text(message):
    bot.send_message(message.chat.id, "Имя вашей команды - " + message.text) # в message.text хранится то, что написал чел



bot.infinity_polling()


