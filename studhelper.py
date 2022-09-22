import telebot
from team import Team
from user import User
from telebot import types


class StudHelperBot:
    token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
    bot = telebot.TeleBot(token)

    def __init__(self):
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)
        self.user = None
        self.team = None

    @staticmethod
    def start():
        StudHelperBot.bot.infinity_polling()


    def start_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Регистрация команды")
        self.user = User(message.from_user.username)
        markup.add(item1)
        self.bot.send_message(message.chat.id, "Привет " + self.user.get_username(), reply_markup=markup)

    def button_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Регистрация команды")
        markup.add(item1)
        self.bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            self.bot.send_message(message.chat.id, "Заполните форму ниже")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg,
                                                self.after_name_of_team_text)  # после сообщения от юзера переходим в функцию

    def after_name_of_team_text(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Удалить команду")
        markup.add(item1)
        msg = self.bot.send_message(message.chat.id, "Имя вашей команды - " + message.text,
                                    reply_markup=markup)  # в message.text хранится то, что написал человек

        self.team = Team(message.text, self.user.get_username())
        self.team.add()

        self.bot.register_next_step_handler(msg, self.after_team_registered_text)

    def after_team_registered_text(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Да")
        item2 = types.KeyboardButton("Нет")
        markup.add(item1)
        markup.add(item2)
        msg = self.bot.send_message(message.chat.id, "Вы точно хотите удалить команду?", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.after_team_delete_text)

    def after_team_delete_text(self, message):
        if message.text == "Да":
            self.bot.send_message(message.chat.id, "Удаляю вашу команду")
            self.team.delete()
        elif message.text == "Нет":
            self.bot.send_message(message.chat.id, "Хорошо")


bot = StudHelperBot()
bot.start()