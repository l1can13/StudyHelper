import telebot
from team import Team
from user import User
from review import Review
from telebot import types
import uuid


class StudHelperBot:
    token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
    bot = telebot.TeleBot(token)

    def __init__(self):
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        # self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)
        self.user = None
        self.team = None
        self.temp_username = None
        self.invited_user = None
        self.review = None
        self.role_of_user = ''
        self.id = 0
        self.tg_name_of_user = ''

    @staticmethod
    def start():
        StudHelperBot.bot.infinity_polling()

    def start_message(self, message):
        self.user = User(None, None, None, message.from_user.username, None, None, message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = 0
        item2 = 0
        if self.user.is_admin():
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            markup.add(item1)
            markup.add(item2)
            self.team = Team(self.user.get_teamname(), self.user.get_id())
            self.bot.send_message(message.chat.id, "Привет, " + self.user.get_username(), reply_markup=markup)
        elif self.user.is_in_team():
            self.user.set_teamname(self.user.get_teamname_from_bd())
            self.user.set_role(self.user.get_role_from_bd())
            self.user.set_name(self.user.get_name_from_bd())
            msg = self.bot.send_message(message.chat.id, "Вы в команде \"" + self.user.get_teamname_from_bd() + "\"")
            if self.user.get_name() is None:
                msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
                self.bot.register_next_step_handler(msg, self.after_name)
            else:
                item1 = types.KeyboardButton("Оценить участников команды")
                item2 = types.KeyboardButton("Отправить отчёт о проделанной работе")
                markup.add(item1)
                markup.add(item2)
                if self.user.get_username() is not None:
                    self.bot.send_message(message.chat.id, "Привет, " + self.user.get_username(), reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, "Привет!", reply_markup=markup)
        else:
            item1 = types.KeyboardButton("Регистрация команды")
            item2 = types.KeyboardButton("Присоединиться к команде")
            markup.add(item1)
            markup.add(item2)
            username = self.user.get_username()
            if username is not None:
                self.bot.send_message(message.chat.id, "Привет, " + self.user.get_username(), reply_markup=markup)
            else:
                self.bot.send_message(message.chat.id, "Привет!", reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            self.bot.send_message(message.chat.id, "Заполните форму ниже")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg, self.product)
        elif message.text == "Добавить участника":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Да")
            item2 = types.KeyboardButton("Нет")
            markup.add(item1)
            markup.add(item2)
            msg = self.bot.send_message(message.chat.id, "Есть ли у вас имя пользователя нового члена команды? ", reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.get_username_to_create_invitation)
        elif message.text == "Оценить участников команды":
            item = types.KeyboardButton("Хорошо")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(item)
            msg = self.bot.send_message(message.chat.id,
                                        'Нужно будет поставить оценки участнику команды и написать про него отзывы',
                                        reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.evaluation)
        elif message.text == "Присоединиться к команде":
            msg = self.bot.send_message(message.chat.id, "Введите ваш код-приглашение: ")
            self.bot.register_next_step_handler(msg, self.accept_invitation)
        elif message.text == "Отправить отчёт о проделанной работе":
            msg = self.bot.send_message(message.chat.id, "Напишите текст вашего отчета: ")
            self.bot.register_next_step_handler(msg, self.report_of_people)
        elif message.text == "Удалить команду":
            item1 = types.KeyboardButton("Регистрация команды")
            item2 = types.KeyboardButton("Присоединиться к команде")

            self.team.delete()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(item1)
            markup.add(item2)
            self.bot.send_message(message.chat.id, "Ваша команда успешно удалена!", reply_markup=markup)

    def get_username_to_create_invitation(self, message):
        if message.text == 'Да':
            msg = self.bot.send_message(message.chat.id, "Введите имя пользователя, соблюдая регистр: ")
            self.bot.register_next_step_handler(msg, self.get_role_to_create_invitation)
        elif message.text == 'Нет':
            self.team.set_team_code(self.create_unique_inv_code())
            self.tg_name_of_user = 'Нет'
            self.bot.send_message(message.chat.id, "Уникальный код участника:  " + self.team.get_team_code())
            msg = self.bot.send_message(message.chat.id, "Этот код необходимо ввести новому участнику")
            # self.bot.send_message(message.chat.id, "Ссылка на бота: t.me/Helping_Student_bot")
            self.get_role_to_create_invitation(message)
        else:
            pass
            #вы написали хуйню

    def get_role_to_create_invitation(self, message):
        self.invited_user = User()
        if self.tg_name_of_user != 'Нет':
            self.tg_name_of_user = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Scrum Master")
        item2 = types.KeyboardButton("Разработчик")
        item3 = types.KeyboardButton("Участник команды")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        msg = self.bot.send_message(message.chat.id, "Выберите роль пользователя: ", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.add_user_to_bd)

    def add_user_to_bd(self, message):
        self.invited_user.set_role(message.text)
        self.invited_user.set_username(self.tg_name_of_user)
        self.invited_user.set_teamname(self.user.get_teamname())
        self.team.add_team_code(self.user.get_teamname(), message.text, self.team.get_team_code())
        self.invited_user.add_user()
        self.bot.send_message(message.chat.id, "Перешлите эту ссылку члену команды: ")
        self.bot.send_message(message.chat.id, "t.me/Helping_Student_bot")

    # def create_invitation(self, message):
    #     self.tg_name_of_user = message.text
    #     self.invited_user.set_role(self.role_of_user)
    #     self.invited_user.set_username(self.tg_name_of_user)
    #     self.invited_user.set_teamname(self.user.get_teamname())
    #     self.invited_user.add_user()
    #     self.bot.send_message(message.chat.id, "Код для приглашения пользователя " +
    #                           self.invited_user.get_username() + ": " +
    #                           str(self.transfer_str_int(message.text)) +
    #                           " \nОтправьте код данному пользователю, чтобы он мог присоединиться к Вашей команде.")


    def create_unique_inv_code(self):
        return str(uuid.uuid1())[:8]

    def accept_invitation(self, message):
        if self.user.check_team_with_code(message.text):  # успешно принимаем в команду
            self.bot.send_message(message.chat.id, "Вы успешно добавлены в команду!")
            self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
            msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
            self.user.set_id(message.from_user.id)
            self.user.set_teamname(self.user.get_team_using_code(message.text))
            self.user.set_role(self.user.get_role_using_code(message.text))
            self.user.update_id_in_bd()
            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.bot.send_message(message.chat.id, "Ваше имя ")

    def name_again(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
        self.bot.register_next_step_handler(msg, self.after_name)

    def after_name(self, message):
        if self.user.get_username() is not None:
            self.user.set_role((self.user.get_role_from_bd()))
            self.user.set_teamname((self.user.get_teamname_from_bd()))
        name = message.text
        noSurname = False
        isSpace = False
        for index, val in enumerate(name):
            if val == ' ':
                isSpace = True
                if index == len(name) - 1:
                    noSurname = True
        if noSurname or not isSpace:
            msg = self.bot.send_message(message.chat.id, "Вы не ввели имя или фамилию, попробуйте еще раз:")
            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.user.set_name(name)
            self.user.add_name()
            msg = self.bot.send_message(message.chat.id, "Введите Вашу группу:")
            self.bot.register_next_step_handler(msg, self.after_group)
            # msg = self.bot.send_message(message.chat.id, "Введите Вашу фамилию:")
            # self.bot.register_next_step_handler(msg, self.after_surname)

    # def after_surname(self, message):
    #     surname = message.text
    #     self.user.set_surname(surname)
    #     self.user.add_surname()
    #     msg = self.bot.send_message(message.chat.id, "Введите Вашу группу:")
    #     self.bot.register_next_step_handler(msg, self.after_group)

    def after_group(self, message):
        group = message.text
        self.user.set_group(group)
        self.user.add_group()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.user.get_role() == 'Product Owner':
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            markup.add(item1, item2)
        item3 = types.KeyboardButton("Оценить участников команды")
        item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
        markup.add(item3, item4)
        msg = self.bot.send_message(message.chat.id, "Ваши данные успешно сохранены!", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.message_reply)

    def product(self, message):  # функция, где запрашивается название продукта и сохраняется в бд имя команды
        name_of_team = message.text
        self.team = Team(name_of_team, self.user.get_id())
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
                              "Команда \"" + self.team.get_name() + "\" успешно зарегистрирована!")  # в message.text хранится то, что написал человек
        self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
        msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
        self.bot.register_next_step_handler(msg, self.after_name)

    def evaluation(self, message):  # функция для оценки участников команды
        team_members = self.team.get_team_members()  # temp - словарь, где ключ - Фамилия, а значения - реальные фамилии
        arr_of_names = []
        for elem in team_members:
            arr_of_names.append(elem['Фамилия'])  # в arr_of_name(список) кладем только сами фамилии
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        if (len(arr_of_names) == 0):
            self.user.set_username(message.from_user.username)
            self.user.set_role((self.user.get_role_from_bd()))
            self.user.set_teamname((self.user.get_teamname_from_bd()))

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.user.get_role() == "Product Owner":
                item1 = types.KeyboardButton("Добавить участника")
                item2 = types.KeyboardButton("Удалить команду")
                markup.add(item1, item2)
            item3 = types.KeyboardButton("Оценить участников команды")
            item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
            markup.add(item3, item4)
            msg = self.bot.send_message(message.chat.id, "У вас нет сокомандников :(", reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.message_reply)
        for elem in arr_of_names:
            item = types.KeyboardButton(elem)
            markup.add(item)

        item = types.KeyboardButton("Отмена")
        markup.add(item)

        msg = self.bot.send_message(message.chat.id, "Выберите члена команды, которого хотите оценить",
                                    reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.after_evaluation)

    def after_evaluation(self, message):  # функция, где участникам ставят общую оценку от 0 до 10
        surname = message.text  # в surname лежит фамилия текущего пользователя

        self.temp_username = self.team.find_username_by_surname(
            surname)  # находим User_name по фамилии (возможно переписать в один запрос, когда ищем фамилию в бд)
        self.review = Review()
        self.review.set_username(self.temp_username)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        if surname != "Отмена":
            for i in range(0, 11):
                item = types.KeyboardButton(str(i))
                markup.add(item)

            self.bot.send_message(message.chat.id, "Оцените участника команды - " + surname)
            estimation = self.bot.send_message(message.chat.id, "Общая оценка: ", reply_markup=markup)
            self.bot.register_next_step_handler(estimation, self.get_gen_mark)
        else:
            self.user.set_username(message.from_user.username)
            self.user.set_role((self.user.get_role_from_bd()))
            self.user.set_teamname((self.user.get_teamname_from_bd()))

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if self.user.get_role() == "Product Owner":
                item1 = types.KeyboardButton("Добавить участника")
                item2 = types.KeyboardButton("Удалить команду")
                markup.add(item1, item2)
            item3 = types.KeyboardButton("Оценить участников команды")
            item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
            markup.add(item3, item4)
            msg = self.bot.send_message(message.chat.id, "Возврат в основное меню...",
                                        reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.message_reply)

    def get_gen_mark(self, message):  # функция, где участникам ставят оценку за решение технических задач от 0 до 10
        general_mark = message.text  # в general_mark лежит общая оценка пользователя
        self.review.set_general_mark(general_mark)
        estimation2 = self.bot.send_message(message.chat.id, "Решение технических задач: ")
        self.bot.register_next_step_handler(estimation2, self.get_t_tasks)

    def get_t_tasks(self, message):  # функция, где участникам ставят оценку за командную работу от 0 до 10
        tech_tasks = message.text  # в tech_tasks лежит оценка пользователя за решение технических задач
        self.review.set_tech_tasks(tech_tasks)
        estimation3 = self.bot.send_message(message.chat.id, "Командная работа: ")
        self.bot.register_next_step_handler(estimation3, self.get_tmwork)

    def get_tmwork(self, message):  # функция, где участникам пишут отзыв об их ответственности
        teamwork = message.text  # в teamwork лежит оценка пользователя за командную работу
        self.review.set_teamwork(teamwork)
        feedback = self.bot.send_message(message.chat.id, "Напишите отзыв о том, насколько был ответственен этот участник команды: ")
        self.bot.register_next_step_handler(feedback, self.get_feedback)

    def get_feedback(self, message):  # функция, где участникам пишут отзыв об их помощи в решении технических задач
        responsibility = message.text  # в responsibility лежит отзыв об ответственности пользователя
        self.review.set_responsibility(responsibility)
        feedback2 = self.bot.send_message(message.chat.id, "Напишите отзыв о том, насколько этот участник команды помогал в решении технических задач: ")
        self.bot.register_next_step_handler(feedback2, self.end_of_evaluation)

    def end_of_evaluation(self, message):
        tech_help = message.text  # в tech_help лежит отзыв о помощи пользователя в решении технических задач
        self.review.set_tech_help(tech_help)
        self.review.add_review()

        self.user.set_username(message.from_user.username)
        self.user.set_role((self.user.get_role_from_bd()))
        self.user.set_teamname((self.user.get_teamname_from_bd()))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.user.get_role() == "Product Owner":
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            markup.add(item1, item2)
        item3 = types.KeyboardButton("Оценить участников команды")
        item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
        markup.add(item3, item4)
        msg = self.bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.message_reply)

    def report_of_people(self, message):
        report = message.text # в report лежит отчет о проделанной работе
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if self.user.get_role() == "Product Owner":
            item1 = types.KeyboardButton("Добавить участника")
            item2 = types.KeyboardButton("Удалить команду")
            markup.add(item1, item2)
        item3 = types.KeyboardButton("Оценить участников команды")
        item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
        markup.add(item3, item4)
        msg = self.bot.send_message(message.chat.id, "Спасибо за Ваш отчёт!", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.message_reply)

bot = StudHelperBot()
bot.start()
