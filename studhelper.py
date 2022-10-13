import telebot
import random
from team import Team
from user import User

from telebot import types


class StudHelperBot:
    token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
    bot = telebot.TeleBot(token)

    def __init__(self):
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        # self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)
        self.user = None
        self.team = None
        self.invited_user = None
        self.role_of_user = ''
        self.tg_name_of_user = ''

    @staticmethod
    def start():
        StudHelperBot.bot.infinity_polling()

    def start_message(self, message):
        self.user = User(None, None, None, message.from_user.username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = 0
        item2 = 0
        if self.user.is_admin():
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            self.team = Team(self.user.get_teamname(), self.user.get_username())
        else:
            item1 = types.KeyboardButton("Регистрация команды")
            item2 = types.KeyboardButton("Присоединиться к команде")

        markup.add(item1)
        markup.add(item2)
        self.bot.send_message(message.chat.id, "Привет, " + self.user.get_username(), reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            self.bot.send_message(message.chat.id, "Заполните форму ниже")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg, self.product)
        elif message.text == "Добавить участника":
            msg = self.bot.send_message(message.chat.id, "Введите роль того, кого хотите пригласить: ")
            self.bot.register_next_step_handler(msg, self.get_role_to_create_invitation)
        elif message.text == "Оценить участников команды":
            item = types.KeyboardButton("Хорошо")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(item)
            msg = self.bot.send_message(message.chat.id, 'Нужно будет поставить оценки всем участникам команды и написать про них отзывы', reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.evaluation)
        elif message.text == "Присоединиться к команде":
            msg = self.bot.send_message(message.chat.id, "Введите ваш код-приглашение: ")
            self.bot.register_next_step_handler(msg, self.accept_invitation)
        elif message.text == "Удалить команду":
            item1 = types.KeyboardButton("Регистрация команды")
            item2 = types.KeyboardButton("Присоединиться к команде")

            self.team.delete()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(item1)
            markup.add(item2)
            msg = self.bot.send_message(message.chat.id, "Ваша команда успешно удалена!", reply_markup=markup)

    def get_role_to_create_invitation(self, message):
        self.invited_user = User()
        self.role_of_user = message.text
        msg = self.bot.send_message(message.chat.id, "Введите имя пользователя этого человека: ")
        self.bot.register_next_step_handler(msg, self.create_invitation)

    def create_invitation(self, message):
        self.tg_name_of_user = message.text
        self.invited_user.set_role(self.role_of_user)
        self.invited_user.set_username(self.tg_name_of_user)
        self.invited_user.set_teamname(self.user.get_teamname())
        self.invited_user.add_user()
        self.bot.send_message(message.chat.id, str(self.transfer_str_int(message.text)))

    def transfer_str_int(self, arg):
        ans = ''
        temp = ''
        if len(arg) % 2:
            while len(arg) < 7:
                arg += 'r'
            for i in range(len(arg)):
                temp += str(ord(arg[i]))
            temp = str(temp)
            for i in range(4):
                ans += arg[-i]
                ans += temp[i]
        else:
            while len(arg) < 7:
                arg += 'l'
            for i in range(len(arg)):
                temp += str(ord(arg[-i]))
            temp = str(temp)
            for i in range(4):
                ans += arg[i]
                ans += temp[-i]
        return ans

    def accept_invitation(self, message):
        if message.text == self.transfer_str_int(self.user.get_username()):  # успешно принимаем в команду
            self.bot.send_message(message.chat.id, "Вы успешно добавлены в команду!")
            self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
            msg = self.bot.send_message(message.chat.id, "Введите Ваше имя:")
            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.bot.send_message(message.chat.id, "Проверьте правильность кода")

    def after_name(self, message):
        self.user.set_role((self.user.get_role_from_bd())['Роль'])
        self.user.set_teamname((self.user.get_teamname_from_bd())['Команда'])
        name = message.text
        self.user.set_name(name)
        self.user.add_name()
        msg = self.bot.send_message(message.chat.id, "Введите Вашу фамилию:")
        self.bot.register_next_step_handler(msg, self.after_surname)

    def after_surname(self, message):
        surname = message.text
        self.user.set_surname(surname)
        self.user.add_surname()
        msg = self.bot.send_message(message.chat.id, "Введите Вашу группу:")
        self.bot.register_next_step_handler(msg, self.after_group)

    def after_group(self, message):
        group = message.text
        self.user.set_group(group)
        self.user.add_group()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.user.get_role() == 'Product Owner':
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            markup.add(item1, item2)
        item = types.KeyboardButton("Оценить участников команды")
        markup.add(item)
        msg = self.bot.send_message(message.chat.id, "Ваши данные успешно сохранены!", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.message_reply)

    def product(self, message):  # функция, где запрашивается название продукта и сохраняется в бд имя команды
        name_of_team = message.text
        self.team = Team(name_of_team, self.user.get_username())
        self.team.add()
        msg = self.bot.send_message(message.chat.id, "Введите название продукта: ")
        self.bot.register_next_step_handler(msg, self.after_product)

    def after_product(self, message):
        self.team.set_product(message.text)
        self.team.add_product()
        self.user.set_teamname(self.team.get_name())
        self.user.set_role("Product Owner")
        self.user.add_user()
        self.bot.send_message(message.chat.id,
                                    "Команда " + self.team.get_name() + " успешно зарегистрирована!")  # в message.text хранится то, что написал человек
        self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
        msg = self.bot.send_message(message.chat.id, "Введите Ваше имя:")
        self.bot.register_next_step_handler(msg, self.after_name)

    def evaluation(self, message): # функция для оценки участников команды
        temp = self.user.get_name_people_of_team() # temp - список словарей, где ключ - Фамилия, а значения - реальные фамилии
        arr_of_name = []
        for i in temp:
            arr_of_name.append(i['Фамилия']) # в arr_of_name(список) кладем только сами фамилии
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item0 = types.KeyboardButton("0")
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        item5 = types.KeyboardButton("5")
        self.team.set_size_of_team(len(arr_of_name))
        markup.add(item0, item1, item2, item3, item4, item5)
        print(self.user.get_counter_of_people())
        estimation = self.bot.send_message(message.chat.id, "Оцените участника команды - " +
                                           arr_of_name[self.user.get_counter_of_people()], reply_markup=markup)
        self.bot.register_next_step_handler(estimation, self.get_estimation)


        #for i in arr_of_name:  # i-ый элемент - фамилия участника, которого оценивают
         #   estimation = self.bot.send_message(message.chat.id, "Оцените участника команды - " + i,
          #                                     reply_markup=markup)
           # self.bot.register_next_step_handler(estimation, self.get_estimation)

    def get_estimation(self, message): # функция, где участникам ставят цифры от 0 до 5
        estimation = int(message.text)  # в estimation лежит интовская оценка участника, ее и можно кинуть в бд
        feedback = self.bot.send_message(message.chat.id, "Напишите отзыв об этом участнике команды")
        self.bot.register_next_step_handler(feedback, self.get_feedback)

    def get_feedback(self, message): # функция, где пишутся отзывы об участниках команды
        feedback = message.text  # в feedback лежит текстовый отзыв об участике команды, его и можно кинуть в бд
        self.user.set_counter_of_people(self.user.get_counter_of_people() + 1)
        if self.user.get_counter_of_people() < self.team.get_size_of_team(): # условный цикл, чтоб оценить всех
            self.evaluation(message)
        self.user.set_counter_of_people(0)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("Ура")
        markup.add(item)
        msg = self.bot.send_message(message.chat.id, "Конец оценивания однокомандников!", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.end_of_evalutation)

    def end_of_evalutation(self, message):
        self.bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!")

bot = StudHelperBot()
bot.start()

