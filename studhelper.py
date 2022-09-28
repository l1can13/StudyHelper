import telebot
from team import Team
from user import User

from telebot import types

class StudHelperBot:
    token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
    bot = telebot.TeleBot(token)

    def __init__(self):
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        #self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)
        self.user = None
        self.team = None

    @staticmethod
    def start():
        StudHelperBot.bot.infinity_polling()

    def start_message(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Регистрация команды")
        self.user = User(None, None, message.from_user.username)
        markup.add(item1)
        self.bot.send_message(message.chat.id, "Привет " + self.user.get_username(), reply_markup=markup)

    #def button_message(self, message):
     #   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      #  item1 = types.KeyboardButton("Регистрация команды")
       # markup.add(item1)
        #self.bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            self.bot.send_message(message.chat.id, "Заполните форму ниже")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg, self.size_of_team)
    def size_of_team(self, message): # функция, где сохраняется в бд имя команды и запрашивается количество человек в команде
        name_of_team = message.text
        self.team = Team(name_of_team, self.user.get_username())
        self.team.add()
        msg = self.bot.send_message(message.chat.id, "Введите количество человек в команде: ")
        self.bot.register_next_step_handler(msg, self.name_of_player)
    def name_of_player(self, message): # функция, где сохраняется в бд количество человек в команде и запрашивается имя участника команды
        self.team.set_size_of_team(int(message.text))
        self.user = User()
        msg = self.bot.send_message(message.chat.id, "Введите имя участника")
        self.bot.register_next_step_handler(msg, self.surname_of_player)
    def name_of_player2(self, message): # фукнция, нужная для цикличности, те когда надо вводить данные о нескольких участниках
        self.user = User()
        msg = self.bot.send_message(message.chat.id, "Введите имя участника")
        self.bot.register_next_step_handler(msg, self.surname_of_player)
    def surname_of_player(self, message): # функция, где сохраняется в бд имя участника команды и запрашивается фамилия участника команды
        self.team.set_counter_of_people(self.team.get_counter_of_people() + 1)
        nm_of_player = message.text
        self.user.set_name(nm_of_player)
        msg = self.bot.send_message(message.chat.id, "Введите фамилию участника")
        self.bot.register_next_step_handler(msg, self.role_of_player)
    def role_of_player(self, message): # функция, где сохраняется в бд фамилия участника команды и запрашивается username из тг участника команды
        surnm_of_player = message.text
        self.user.set_surname(surnm_of_player)
        msg = self.bot.send_message(message.chat.id, "Введите username участника")
        self.bot.register_next_step_handler(msg, self.username_of_player)
    def username_of_player(self, message): # функция, где сохраняется в бд username из тг участника команды и запрашивается роль участника команды
        usrnm_of_player = message.text
        self.user.set_username(usrnm_of_player)
        msg = self.bot.send_message(message.chat.id, "Введите роль участника")
        self.bot.register_next_step_handler(msg, self.end_of_info_about_one_player)
    def end_of_info_about_one_player(self, message): # тут есть ветки, прыгаем в одну, если ввели всех участников, и в другую, если еще не всех
        rl_of_player = message.text
        self.user.set_role(rl_of_player)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Далее")
        markup.add(item1)
        msg = self.bot.send_message(message.chat.id, "Конец заполнения человека! Нажмите далее, чтобы продолжить", reply_markup=markup)
        self.user.set_teamname(self.team.get_name())
        self.user.add_user()
        if self.team.get_counter_of_people() == self.team.get_size_of_team():
            self.bot.register_next_step_handler(msg, self.after_name_of_team_text)
        else:
            self.bot.register_next_step_handler(msg, self.name_of_player2)

    def after_name_of_team_text(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Удалить команду")
        markup.add(item1)
        msg = self.bot.send_message(message.chat.id, "Команда " + self.user.get_teamname() + " успешно зарегистрирована!",
                                    reply_markup=markup)  # в message.text хранится то, что написал человек
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