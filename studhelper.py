import telebot
from telebot import types


class StudHelperBot:
    token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
    bot = telebot.TeleBot(token)

    def __init__(self):
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)

    @staticmethod
    def start():
        StudHelperBot.bot.infinity_polling()

    def start_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Регистрация команды")
        markup.add(item1)
        self.bot.send_message(message.chat.id, "Тест. Привет", reply_markup=markup)

    def button_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Регистрация команды")
        markup.add(item1)
        self.bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            self.bot.send_message(message.chat.id, "Заполните форму ниже")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg, self.after_name_of_team_text)  # после сообщения от юзера переходим в функцию

    def after_name_of_team_text(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Удалить команду")
        markup.add(item1)
        item2 = types.KeyboardButton("Добавить участника")
        markup.add(item2)
        item3 = types.KeyboardButton("Удалить участника")
        markup.add(item3)
        msg = self.bot.send_message(message.chat.id, "Имя вашей команды - " + message.text,
                               reply_markup=markup)  # в message.text хранится то, что написал чел
        self.bot.register_next_step_handler(msg, self.after_team_registered_text)

    def after_team_registered_text(self, message):
        if message.text == "Удалить команду":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Да")
            item2 = types.KeyboardButton("Нет")
            markup.add(item1)
            markup.add(item2)
            msg = self.bot.send_message(message.chat.id, "Вы точно хотите удалить команду?", reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.after_team_delete_text)
        elif message.text == "Добавить участника":
            msg = self.bot.send_message(message.chat.id, "Укажите ID нового участника")
            self.bot.register_next_step_handler(msg, self.add_new_team_member)
        elif message.text == "Удалить участника":
            msg = self.bot.send_message(message.chat.id, "Выберите участника которого хотите удалить")
            self.bot.register_next_step_handler(msg, self.delete_team_member)

    def after_team_delete_text(self, message):
        if message.text == "Да":
            # team = get_team_from_bd() ? находим эту команду в бд по айди админа ?
            self.bot.send_message(message.chat.id, "Удаляю вашу команду ")
            # delete_team_from_bd(team) ? удаляем эту команду из бд ?
        elif message.text == "Нет":
            self.bot.send_message(message.chat.id, "Хорошо")

    def add_new_team_member(self, message):
        pass

    def delete_team_member(self, message):
        pass
        # появляется выбор участника, кроме самого админа


bot = StudHelperBot()
bot.start()


