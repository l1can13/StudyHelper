import telebot
from telebot.types import ReplyKeyboardRemove

from report import Report
from team import Team
from user import User
from review import Review
from telebot import types
import uuid
from datetime import datetime


def create_unique_inv_code():
    return str(uuid.uuid1())[:8]


class StudHelperBot:

    def __init__(self):
        self.token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"
        self.bot = telebot.TeleBot(self.token)
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
        # self.button_message = self.bot.message_handler(commands=['button'])(self.button_message)
        self.message_reply = self.bot.message_handler(content_types='text')(self.message_reply)
        self.user_dict = {}
        self.invited_user_dict = {}
        self.team_dict = {}
        self.review_dict = {}
        self.temp_username_dict = {}
        self.tg_name_of_user_dict = {}
        self.first_hello_dict = {}
        self.report_dict = {}
        self.sprint_now = ''
        self.roles = ["Product owner", "Scrum Master", "Разработчик", "Участник команды"]
        self.sprints = ["Спринт №0", "Спринт №1", "Спринт №2", "Спринт №3", "Спринт №4", "Спринт №5", "Спринт №6"]

    def start(self):
        self.bot.infinity_polling()

    def start_message(self, message):
        self.user_dict[message.chat.id] = User(None, None, None, message.from_user.username, None, None,
                                               message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.tg_name_of_user_dict[message.chat.id] = ''
        self.first_hello_dict[message.chat.id] = self.user_dict[message.chat.id].is_in_team()
        item1 = 0
        item3 = 0
        item4 = 0
        if " " in message.text and not self.first_hello_dict[message.chat.id] and message.text != 'Отмена регистрации':
            message.text = message.text.split()[1]
            self.accept_invitation(message)
        else:
            if self.user_dict[message.chat.id].is_admin():
                item1 = types.KeyboardButton("Добавить участника")
                # item3 = types.KeyboardButton("Оценить участников команды")
                item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
                item5 = types.KeyboardButton("Помощь")
                markup.add(item1)
                # markup.add(item3)
                markup.add(item4)
                markup.add(item5)
                self.team_dict[message.chat.id] = Team(self.user_dict[message.chat.id].get_teamname_from_bd(),
                                                       self.user_dict[message.chat.id].get_db_id())
                self.user_dict[message.chat.id].set_teamname(self.team_dict[message.chat.id].get_teamname())
            elif self.user_dict[message.chat.id].is_in_team():
                self.user_dict[message.chat.id].set_teamname(self.user_dict[message.chat.id].get_teamname_from_bd())
                self.user_dict[message.chat.id].set_role(self.user_dict[message.chat.id].get_role_from_bd())
                self.user_dict[message.chat.id].set_name(self.user_dict[message.chat.id].get_name_from_bd())
                if self.user_dict[message.chat.id].get_name() is None:
                    msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
                    self.bot.register_next_step_handler(msg, self.after_name)
                    return
                else:
                    # item1 = types.KeyboardButton("Оценить участников команды")
                    item2 = types.KeyboardButton("Отправить отчёт о проделанной работе")
                    item5 = types.KeyboardButton("Помощь")
                    # markup.add(item1)
                    markup.add(item2)
                    markup.add(item5)
            else:
                item1 = types.KeyboardButton("Регистрация команды")
                item5 = types.KeyboardButton("Помощь")
                markup.add(item1)
                markup.add(item5)
            if not self.first_hello_dict[message.chat.id]:
                if self.user_dict[message.chat.id].get_username() is not None:
                    self.bot.send_message(message.chat.id, "Привет, " + self.user_dict[message.chat.id].get_username(),
                                          reply_markup=markup)
                else:
                    self.bot.send_message(message.chat.id, "Привет!", reply_markup=markup)
                self.first_hello_dict[message.chat.id] = True
            else:
                self.bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Отмена регистрации")
            item2 = types.KeyboardButton("Продолжить регистрацию")
            markup.add(item1, item2)
            msg = self.bot.send_message(message.chat.id, "Внимание! Команду должен регистрировать Scrum Master! Если Вы не являетесь Scrum Master'ом, то нажмите кнопку 'Отмена регистрации'. Если являетесь - нажмите кнопку 'Продолжить регистрацию'", reply_markup=markup)
        elif message.text == "Помощь":
            msg = self.bot.send_message(message.chat.id, "Возникла проблема с ботом, или нашли баг?\n\nНапишите @l1can для получения информации по боту, а также для решения любой проблемы (как создать команду, переименование/удаление команды, удаление участников, переименование/удаление продукта, и т.д)",
                                        reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Добавить участника":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Да")
            item2 = types.KeyboardButton("Нет")
            markup.add(item1)
            markup.add(item2)
            self.get_role_to_create_invitation(message)
        # elif message.text == "Оценить участников команды":
        #     item = types.KeyboardButton("Хорошо")
        #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #     markup.add(item)
        #     msg = self.bot.send_message(message.chat.id,
        #                                 'Нужно будет поставить оценки участнику команды и написать про него отзывы',
        #                                 reply_markup=markup)
        #     self.bot.register_next_step_handler(msg, self.evaluation)
        elif message.text == "Отправить отчёт о проделанной работе":  # Сначала выбираем спринт, потом уже пишем текст отчета
            self.choose_sprint_on_review(message)
            # msg = self.bot.send_message(message.chat.id, "Напишите текст вашего отчета: ",
            #                             reply_markup=ReplyKeyboardRemove())
            # self.bot.register_next_step_handler(msg, self.report_of_people)
        elif message.text.lower() == "обновить":
            msg = self.bot.send_message(message.chat.id, "Обновляю состояние бота...",
                                        reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Отмена регистрации":
            msg = self.bot.send_message(message.chat.id, "Возврат к главному меню", reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Продолжить регистрацию":
            self.bot.send_message(message.chat.id, "Заполните форму ниже", reply_markup=ReplyKeyboardRemove())
            # msg = self.bot.send_message(message.chat.id, "Введите имя команды: ", reply_markup=ReplyKeyboardRemove())
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ")
            self.bot.register_next_step_handler(msg, self.set_team_name)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.start_message(message)

    def choose_sprint_on_review(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(self.sprints[0])
        item2 = types.KeyboardButton(self.sprints[1])
        item3 = types.KeyboardButton(self.sprints[2])
        item4 = types.KeyboardButton(self.sprints[3])
        item5 = types.KeyboardButton(self.sprints[4])
        item6 = types.KeyboardButton(self.sprints[5])
        item7 = types.KeyboardButton(self.sprints[6])
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        markup.add(item7)
        msg = self.bot.send_message(message.chat.id, "Выберите спринт (меню с кнопками можно пролистать): ", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.set_sprint)

    def set_sprint(self, message):
        if message.text in self.sprints:
            self.sprint_now = message.text  # будет в формате "Спринт №1"/"Спринт №2" и тд
            msg = self.bot.send_message(message.chat.id, "Напишите текст вашего отчета: ",
                                        reply_markup=ReplyKeyboardRemove())
            self.bot.register_next_step_handler(msg, self.report_of_people)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(", reply_markup=ReplyKeyboardRemove())
            self.choose_sprint_on_review(message)

    def get_role_to_create_invitation(self, message):
        self.team_dict[message.chat.id].set_team_code(create_unique_inv_code())
        # self.invited_user_dict[message.chat.id] = User()
        # if self.tg_name_of_user_dict[message.chat.id] != 'Нет':
        #     self.tg_name_of_user_dict[message.chat.id] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(self.roles[0])
        item2 = types.KeyboardButton(self.roles[1])
        item3 = types.KeyboardButton(self.roles[2])
        item4 = types.KeyboardButton(self.roles[3])
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        msg = self.bot.send_message(message.chat.id, "Выберите роль пользователя: ", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.add_user_to_bd)

    def add_user_to_bd(self, message):
        if message.text not in self.roles:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.get_role_to_create_invitation(message)
            return
        # self.invited_user_dict[message.chat.id].set_role(message.text)
        # # self.invited_user.set_username(self.tg_name_of_user_dict[message.chat.id])
        # self.invited_user_dict[message.chat.id].set_teamname(self.user_dict[message.chat.id].get_teamname())
        # self.invited_user_dict[message.chat.id].add_user()
        self.team_dict[message.chat.id].add_team_code(message.text,
                                                      self.team_dict[message.chat.id].get_team_code())
        self.bot.send_message(message.chat.id,
                              "Для того, чтобы приглашенный участник смог присоединиться к команде, ему необходимо ввести данную ссылку: ")
        self.bot.send_message(message.chat.id, "https://t.me/Helping_Student_bot?start=" + self.team_dict[
            message.chat.id].get_team_code())
        self.bot.send_message(message.chat.id, "Команда и роль будут определены автоматически")
        self.start_message(message)

    def accept_invitation(self, message):
        if self.user_dict[message.chat.id].check_team_with_code(message.text):  # успешно принимаем в команду
            self.user_dict[message.chat.id].set_tg_id(message.from_user.id)
            self.user_dict[message.chat.id].set_invite_code(message.text)
            self.user_dict[message.chat.id].set_teamname(
                self.user_dict[message.chat.id].get_team_using_code(message.text))
            self.user_dict[message.chat.id].set_role(self.user_dict[message.chat.id].get_role_using_code(message.text))

            self.user_dict[message.chat.id].add_user()

            self.bot.send_message(message.chat.id, "Вы успешно добавлены в команду \"" + self.user_dict[
                message.chat.id].get_teamname() + "\"!",
                                  reply_markup=ReplyKeyboardRemove())
            self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
            msg = self.bot.send_message(message.chat.id, "Введите имя в формате Фамилия Имя:")

            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.bot.send_message(message.chat.id,
                                  "Некорректный код или некорректная ссылка, пожалуйста, попробуйте еще раз")
            self.start_message(message)

    def name_again(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите имя в формате Фамилия Имя:")
        self.bot.register_next_step_handler(msg, self.after_name)

    def after_name(self, message):
        name = message.text
        no_surname = False
        is_space = False
        for index, val in enumerate(name):
            if val == ' ':
                is_space = True
                if index == len(name) - 1:
                    no_surname = True
        if no_surname or not is_space:
            msg = self.bot.send_message(message.chat.id, "Вы не ввели имя или фамилию, попробуйте еще раз:")
            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.user_dict[message.chat.id].set_name(name)
            msg = self.bot.send_message(message.chat.id, "Введите номер Вашей группы в формате XXXX:")
            self.bot.register_next_step_handler(msg, self.after_group)

    def after_group(self, message):
        group = message.text
        self.user_dict[message.chat.id].set_group(group)
        if message.from_user.username is not None:
            self.user_dict[message.chat.id].set_username(message.from_user.username)

        if self.user_dict[message.chat.id].get_invite_code() == 'admin':
            self.user_dict[message.chat.id].add_user_to_team_members()  # добавляем пользователя в таблицу team_members.
        else:
            self.user_dict[message.chat.id].update_user_id_in_team_members() # обновляем user_id - ТОЛЬКО ДЛЯ
            # ПРИГЛАШЕННЫХ ПОЛЬЗОВАТЕЛЕЙ, т.к. невозможно получить user_id из таблицы users до того, как мы его туда
            # добавим

        # P.S. Делаю отдельно, так как в team_members нужен db_id, который можно получить только после добавления
        # пользователя в таблицу users

        self.user_dict[message.chat.id].add_name()
        self.user_dict[message.chat.id].add_group()

        self.bot.send_message(message.chat.id, "Ваши данные успешно сохранены!")
        self.start_message(message)

    def set_team_name(self, message):  # функция, где запрашивается название продукта и сохраняется в бд имя команды
        name_of_team = message.text
        if Team.check_teamname_for_unique(name_of_team):  # проверяем по бд уникальность названия команды
            self.team_dict[message.chat.id] = Team()
            self.team_dict[message.chat.id].set_teamname(name_of_team)
            if self.user_dict[message.chat.id].get_username() is None:
                self.user_dict[message.chat.id].set_username('no_username')

            self.user_dict[message.chat.id].set_invite_code(
                'admin')  # сетаем инвайт код для админа - то есть его нет (для понятности оставил слово admin, можно будет поменять)
            self.write_product_name(message)
        else:
            self.bot.send_message(message.chat.id, "Такое имя команды уже существует")
            self.bot.send_message(message.chat.id, "Пожалуйста, выберите другое имя")
            msg = self.bot.send_message(message.chat.id, "Введите имя команды: ", reply_markup=ReplyKeyboardRemove())
            self.bot.register_next_step_handler(msg, self.set_team_name)

    def write_product_name(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите название продукта: ", reply_markup=ReplyKeyboardRemove())
        self.bot.register_next_step_handler(msg, self.after_product)

    def after_product(self, message):
        product_name = message.text
        if Team.check_product_for_unique(product_name):
            self.user_dict[message.chat.id].add_user()  # добавляем пользователя в таблицу users

            self.team_dict[message.chat.id].set_product(product_name)
            self.team_dict[message.chat.id].set_admin(self.user_dict[message.chat.id].get_db_id())

            self.team_dict[message.chat.id].add()  # добавляем команду в бд, добавляется название, юзернейм админа его ид в тг, название продукта
            self.user_dict[message.chat.id].set_teamname(self.team_dict[message.chat.id].get_teamname())
            self.user_dict[message.chat.id].set_role("Scrum Master")  # Scrum Master
            self.bot.send_message(message.chat.id,
                                  "Команда \"" + self.team_dict[
                                      message.chat.id].get_teamname() + "\" успешно зарегистрирована!")  # в message.text хранится то, что написал человек
            self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
            msg = self.bot.send_message(message.chat.id, "Введите имя в формате Фамилия Имя:")
            self.bot.register_next_step_handler(msg, self.after_name)
        else:
            self.bot.send_message(message.chat.id, "Такое имя для продукта уже существует")
            self.bot.send_message(message.chat.id, "Пожалуйста, выберите другое имя")
            self.write_product_name(message)

    # def evaluation(self, message):  # функция для оценки участников команды
    #     team_members = self.team.get_team_members()  # temp - словарь, где ключ - Фамилия, а значения - реальные фамилии
    #     arr_of_names = []
    #     for elem in team_members:
    #         arr_of_names.append(elem['Имя'])  # в arr_of_name(список) кладем только сами фамилии
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     if len(arr_of_names) == 0:
    #         self.user.set_username(message.from_user.username)
    #         self.user.set_role((self.user.get_role_from_bd()))
    #         self.user.set_teamname((self.user.get_teamname_from_bd()))
    #         self.bot.send_message(message.chat.id, "У вас нет сокомандников :(", reply_markup=markup)
    #         self.start_message(message)
    #     for elem in arr_of_names:
    #         item = types.KeyboardButton(elem)
    #         markup.add(item)
    #     item = types.KeyboardButton("Отмена")
    #     markup.add(item)
    #
    #     msg = self.bot.send_message(message.chat.id, "Выберите члена команды, которого хотите оценить",
    #                                 reply_markup=markup)
    #     self.bot.register_next_step_handler(msg, self.after_evaluation)
    #
    # def after_evaluation(self, message):  # функция, где участникам ставят общую оценку от 0 до 10
    #     surname = message.text  # в surname лежит фамилия текущего пользователя
    #
    #     self.temp_username_dict[message.chat.id] = self.team.find_username_by_surname(
    #         surname)  # находим User_name по фамилии (возможно переписать в один запрос, когда ищем фамилию в бд)
    #     self.review = Review()
    #     self.review.set_username(self.temp_username_dict[message.chat.id])
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #
    #     if surname != "Отмена":
    #         for i in range(0, 11):
    #             item = types.KeyboardButton(str(i))
    #             markup.add(item)
    #
    #         self.bot.send_message(message.chat.id, "Оцените участника команды - " + surname)
    #         estimation = self.bot.send_message(message.chat.id, "Общая оценка: ", reply_markup=markup)
    #         self.bot.register_next_step_handler(estimation, self.get_gen_mark)
    #     else:
    #         self.user.set_username(message.from_user.username)
    #         self.user.set_role((self.user.get_role_from_bd()))
    #         self.user.set_teamname((self.user.get_teamname_from_bd()))
    #         self.start_message(message)
    #
    # def get_gen_mark(self, message):  # функция, где участникам ставят оценку за решение технических задач от 0 до 10
    #     general_mark = message.text  # в general_mark лежит общая оценка пользователя
    #     self.review.set_general_mark(general_mark)
    #     estimation2 = self.bot.send_message(message.chat.id, "Решение технических задач: ")
    #     self.bot.register_next_step_handler(estimation2, self.get_t_tasks)
    #
    # def get_t_tasks(self, message):  # функция, где участникам ставят оценку за командную работу от 0 до 10
    #     tech_tasks = message.text  # в tech_tasks лежит оценка пользователя за решение технических задач
    #     self.review.set_tech_tasks(tech_tasks)
    #     estimation3 = self.bot.send_message(message.chat.id, "Командная работа: ")
    #     self.bot.register_next_step_handler(estimation3, self.get_tmwork)
    #
    # def get_tmwork(self, message):  # функция, где участникам пишут отзыв об их ответственности
    #     teamwork = message.text  # в teamwork лежит оценка пользователя за командную работу
    #     self.review.set_teamwork(teamwork)
    #     feedback = self.bot.send_message(message.chat.id, "Напишите отзыв о том, насколько был ответственен этот участник команды: ")
    #     self.bot.register_next_step_handler(feedback, self.get_feedback)
    #
    # def get_feedback(self, message):  # функция, где участникам пишут отзыв об их помощи в решении технических задач
    #     responsibility = message.text  # в responsibility лежит отзыв об ответственности пользователя
    #     self.review.set_responsibility(responsibility)
    #     feedback2 = self.bot.send_message(message.chat.id, "Напишите отзыв о том, насколько этот участник команды помогал в решении технических задач: ")
    #     self.bot.register_next_step_handler(feedback2, self.end_of_evaluation)
    #
    # def end_of_evaluation(self, message):
    #     tech_help = message.text  # в tech_help лежит отзыв о помощи пользователя в решении технических задач
    #     self.review.set_tech_help(tech_help)
    #
    #     current_date = datetime.now()
    #     self.review.set_date(current_date)
    #     self.review.set_reviewer(self.user.get_username())
    #
    #     self.review.add_review()
    #
    #     self.user.set_username(message.from_user.username)
    #     self.user.set_role((self.user.get_role_from_bd()))
    #     self.user.set_teamname((self.user.get_teamname_from_bd()))
    #     self.bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!")
    #     self.start_message(message)

    def report_of_people(self, message):
        departure_time = datetime.now()
        report = message.text  # в report лежит отчет о проделанной работе
        self.report_dict[message.chat.id] = Report()
        self.report_dict[message.chat.id].set_report(report)
        self.report_dict[message.chat.id].set_sprint(int(self.sprint_now[len(self.sprint_now) - 1]))
        self.report_dict[message.chat.id].set_date(departure_time)
        self.report_dict[message.chat.id].set_user(self.user_dict[message.chat.id].get_db_id())
        self.report_dict[message.chat.id].add_report()
        self.bot.send_message(message.chat.id, "Спасибо за Ваш отчёт!")
        self.start_message(message)


bot = StudHelperBot()
bot.start()
