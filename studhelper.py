import traceback

import telebot
from telebot.types import ReplyKeyboardRemove

from report import Report
from team import Team
from user import User
from telebot import types
from pymysql import IntegrityError
import uuid
from datetime import datetime


def create_unique_inv_code():
    return str(uuid.uuid1())[:8]


def continue_cancel_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton("Изменить")
    item2 = types.KeyboardButton("Продолжить")
    item3 = types.KeyboardButton("Отменить")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    return markup


class StudHelperBot:

    def __init__(self):
        # self.token = "5102428240:AAF-GZ5AbcbYVPlCnBG_qwFCrhLiWIPgXIE"  # prod
        self.token = "5954982537:AAFgZ5CIpv7HpfyqXXpyVJups0wCZWbCYFQ"  # dev
        self.bot = telebot.TeleBot(self.token)
        self.start_message = self.bot.message_handler(commands=['start'])(self.start_message)
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
        self.sprints = ["Спринт №1", "Спринт №2", "Спринт №3", "Спринт №4", "Спринт №5", "Спринт №6"]

    def update(self, message):
        if " " in message.text:
            self.user_dict[message.chat.id] = User(None, None, None, message.from_user.username, None, None,
                                                   message.from_user.id)
            try:
                self.team_dict[message.chat.id] = Team(Team.get_teamname_by_code(message.text.split()[1]),
                                                       Team.get_user_id_by_code(message.text.split()[1]))
            except TypeError:
                self.team_dict[message.chat.id] = Team(None, None)

            self.tg_name_of_user_dict[message.chat.id] = ''
            self.first_hello_dict[message.chat.id] = self.user_dict[message.chat.id].is_in_team()
        else:
            self.user_dict[message.chat.id] = User(None, None, None, message.from_user.username, None, None,
                                                   message.from_user.id)
            try:
                self.team_dict[message.chat.id] = Team(self.user_dict[message.chat.id].get_teamname_from_bd(),
                                                       self.user_dict[message.chat.id].get_db_id())
            except TypeError:
                self.team_dict[message.chat.id] = Team(None, None)

            self.team_dict[message.chat.id].set_team_code(create_unique_inv_code())
            self.tg_name_of_user_dict[message.chat.id] = ''
            self.first_hello_dict[message.chat.id] = self.user_dict[message.chat.id].is_in_team()

    def start(self):
        self.bot.infinity_polling()

    def start_message(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        if " " in message.text and not self.first_hello_dict[message.chat.id] and message.text != 'Отмена регистрации':
            message.text = message.text.split()[1]
            self.accept_invitation(message)
        else:
            if self.user_dict[message.chat.id].is_admin():
                item1 = types.KeyboardButton("Добавить участника")
                item4 = types.KeyboardButton("Отправить отчёт о проделанной работе")
                item5 = types.KeyboardButton("Помощь")
                markup.add(item1)
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
                    item2 = types.KeyboardButton("Отправить отчёт о проделанной работе")
                    item5 = types.KeyboardButton("Помощь")
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
            self.bot.send_message(message.chat.id,
                                  "Внимание! Команду должен регистрировать Scrum Master! Если Вы не являетесь "
                                  "Scrum Master'ом, то нажмите кнопку 'Отмена регистрации'. Если являетесь - "
                                  "нажмите кнопку 'Продолжить регистрацию'",
                                  reply_markup=markup)
        elif message.text == "Помощь":
            self.bot.send_message(message.chat.id,
                                  "Возникла проблема с ботом, или нашли баг?\n\nНапишите @l1can для получения "
                                  "информации по боту, а также для решения любой проблемы (как создать команду, "
                                  "переименование/удаление команды, удаление участников, "
                                  "переименование/удаление продукта, и т.д)")
            self.start_message(message)
        elif message.text == "Добавить участника":
            self.get_role_to_create_invitation(message)
        elif message.text == "Отправить отчёт о проделанной работе":  # Сначала выбираем спринт, потом уже пишем текст отчета
            self.choose_sprint_on_review(message)
        elif message.text.lower() == "обновить":
            self.bot.send_message(message.chat.id, "Обновляю состояние бота...",
                                  reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Отмена регистрации":
            self.bot.send_message(message.chat.id, "Возврат к главному меню", reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Продолжить регистрацию":
            self.team_registration(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.start_message(message)

    def team_registration(self, message):
        self.bot.send_message(message.chat.id, "Заполните форму ниже", reply_markup=ReplyKeyboardRemove())
        msg = self.bot.send_message(message.chat.id, "Введите название команды: ")
        self.bot.register_next_step_handler(msg, self.enter_team_name)

    def choose_sprint_on_review(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(self.sprints[0])
        item2 = types.KeyboardButton(self.sprints[1])
        item3 = types.KeyboardButton(self.sprints[2])
        item4 = types.KeyboardButton(self.sprints[3])
        item5 = types.KeyboardButton(self.sprints[4])
        item6 = types.KeyboardButton(self.sprints[5])
        item7 = types.KeyboardButton('Отменить')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        markup.add(item7)
        msg = self.bot.send_message(message.chat.id, "Выберите спринт (меню с кнопками можно пролистать): ",
                                    reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.set_sprint)

    def set_sprint(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        if message.text.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода номера спринта.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        if message.text in self.sprints:
            self.sprint_now = message.text  # будет в формате "Спринт №1"/"Спринт №2" и тд
            msg = self.bot.send_message(message.chat.id, "Напишите текст вашего отчета: ",
                                        reply_markup=ReplyKeyboardRemove())
            self.bot.register_next_step_handler(msg, self.report_of_people)
        elif message.text == 'Отменить':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(", reply_markup=ReplyKeyboardRemove())
            self.choose_sprint_on_review(message)

    def get_role_to_create_invitation(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        self.team_dict[message.chat.id].set_team_code(create_unique_inv_code())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(self.roles[0])
        item2 = types.KeyboardButton(self.roles[1])
        item3 = types.KeyboardButton(self.roles[2])
        item4 = types.KeyboardButton(self.roles[3])
        item5 = types.KeyboardButton('Отменить')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        msg = self.bot.send_message(message.chat.id, "Выберите роль пользователя: ", reply_markup=markup)
        self.bot.register_next_step_handler(msg, self.add_user_to_bd)

    def add_user_to_bd(self, message):
        if message.text == 'Отменить':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        elif message.text not in self.roles:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.get_role_to_create_invitation(message)
            return

        try:
            new_user_id = User.add_empty_user()

            self.team_dict[message.chat.id].add_team_code(new_user_id,
                                                          message.text,
                                                          self.team_dict[message.chat.id].get_team_code())
            self.bot.send_message(message.chat.id,
                                  "Для того, чтобы приглашенный участник смог присоединиться к команде, ему необходимо "
                                  "ввести данную ссылку: ")
            # self.bot.send_message(message.chat.id, "https://t.me/Helping_Student_bot?start=" + self.team_dict[
            #     message.chat.id].get_team_code()) # prod
            self.bot.send_message(message.chat.id, "https://t.me/StudHelperDevBot?start=" + self.team_dict[
                message.chat.id].get_team_code())  # dev
            self.bot.send_message(message.chat.id, "Команда и роль будут определены автоматически")
            self.start_message(message)
        except IntegrityError as e:
            print(traceback.format_exc())
            self.bot.send_message(message.chat.id, "Кажется, информация о Вашей команде отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def accept_invitation(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        if self.user_dict[message.chat.id].check_team_with_code(message.text):  # успешно принимаем в команду
            self.user_dict[message.chat.id].set_tg_id(message.from_user.id)
            self.user_dict[message.chat.id].set_invite_code(message.text)
            self.user_dict[message.chat.id].set_teamname(
                self.user_dict[message.chat.id].get_team_using_code(message.text))
            self.user_dict[message.chat.id].set_role(self.user_dict[message.chat.id].get_role_using_code(message.text))

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

    def enter_group_num(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите номер Вашей группы в формате XXXX:",
                                    reply_markup=ReplyKeyboardRemove())
        self.bot.register_next_step_handler(msg, self.after_group)

    def set_user_name(self, message, name):
        self.user_dict[message.chat.id].set_name(name)
        self.enter_group_num(message)

    def after_name(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        name = message.text

        if name.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода своего ФИО.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

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
            markup = continue_cancel_buttons()

            msg = self.bot.send_message(message.chat.id,
                                        f"Проверьте правильность ввода\n\n"
                                        f"Ваше ФИО: {name}",
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.confirm_enter, self.set_user_name, name)

    def enter_user_name(self, message):
        self.bot.send_message(message.chat.id, "Пожалуйста, заполните информацию о себе")
        msg = self.bot.send_message(message.chat.id, "Введите имя в формате Фамилия Имя:",
                                    reply_markup=ReplyKeyboardRemove())
        self.bot.register_next_step_handler(msg, self.after_name)

    def set_group_num(self, message, group):
        try:
            self.user_dict[message.chat.id].set_group(group)

            if self.user_dict[message.chat.id].get_invite_code() != 'admin':
                self.user_dict[message.chat.id].update_invited_user(
                    Team.get_user_id_by_code(self.user_dict[message.chat.id].get_invite_code()))
            else:
                self.user_dict[message.chat.id].add()

                self.team_dict[message.chat.id].set_admin(self.user_dict[message.chat.id].get_db_id())
                self.team_dict[
                    message.chat.id].add()  # добавляем команду в бд, добавляется название, юзернейм админа его ид в тг, название продукта

            if message.from_user.username is not None:
                self.user_dict[message.chat.id].set_username(message.from_user.username)

            if self.user_dict[message.chat.id].get_invite_code() == 'admin':
                self.user_dict[
                    message.chat.id].add_user_to_team_members()  # добавляем пользователя в таблицу team_members.
            else:
                self.user_dict[message.chat.id].update_user_id_in_team_members()  # обновляем user_id - ТОЛЬКО ДЛЯ
                # ПРИГЛАШЕННЫХ ПОЛЬЗОВАТЕЛЕЙ, т.к. невозможно получить user_id из таблицы users до того, как мы его туда
                # добавим

            # P.S. Делаю отдельно, так как в team_members нужен db_id, который можно получить только после добавления
            # пользователя в таблицу users

            self.bot.send_message(message.chat.id, "Ваши данные успешно сохранены!")
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вас отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def after_group(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        group = message.text

        if group.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода номера Вашей группы.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        markup = continue_cancel_buttons()

        msg = self.bot.send_message(message.chat.id,
                                    f"Проверьте правильность ввода\n\n"
                                    f"Ваша группа: {group}",
                                    reply_markup=markup)

        self.bot.register_next_step_handler(msg, self.confirm_enter, self.set_group_num, group)

    def set_team_name(self, message, name_of_team):
        self.team_dict[message.chat.id] = Team()
        self.team_dict[message.chat.id].set_teamname(name_of_team)
        if self.user_dict[message.chat.id].get_username() is None:
            self.user_dict[message.chat.id].set_username('no_username')

        self.user_dict[message.chat.id].set_invite_code(
            'admin')  # сетаем инвайт код для админа - то есть его нет (для понятности оставил слово admin, можно будет поменять)
        self.enter_product_name(message)

    def confirm_enter(self, message, callback, *args):
        edit = None

        if callback == self.set_team_name:
            edit = self.team_registration
        elif callback == self.set_product_name:
            edit = self.enter_product_name
        elif callback == self.set_user_name:
            edit = self.enter_user_name
        elif callback == self.set_group_num:
            edit = self.enter_group_num
        elif callback == self.set_report_text:
            edit = self.choose_sprint_on_review
        else:
            self.bot.send_message(message.chat.id, "Произошла непредвиденная ошибка, попробуйте снова!")
            self.start_message(message)

        if message.text == 'Изменить':
            edit(message)
        elif message.text == 'Продолжить':
            callback(message, args[0])
        elif message.text == 'Отменить':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(. Попробуйте снова.")
            edit(message)

    def enter_team_name(self, message):  # функция, где запрашивается название продукта и сохраняется в бд имя команды
        if message.chat.id not in self.user_dict:
            self.update(message)

        name_of_team = message.text

        if name_of_team.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода названия команды.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        if Team.check_teamname_for_unique(name_of_team):  # проверяем по бд уникальность названия команды
            markup = continue_cancel_buttons()

            msg = self.bot.send_message(message.chat.id,
                                        f"Проверьте правильность ввода\n\n"
                                        f"Название команды: {name_of_team}",
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.confirm_enter, self.set_team_name, name_of_team)
        else:
            self.bot.send_message(message.chat.id, "Такое имя команды уже существует\n"
                                                   "Пожалуйста, выберите другое имя")
            self.team_registration(message)

    def enter_product_name(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите название продукта: ", reply_markup=ReplyKeyboardRemove())
        self.bot.register_next_step_handler(msg, self.after_product)

    def set_product_name(self, message, product_name):
        self.team_dict[message.chat.id].set_product(product_name)

        self.user_dict[message.chat.id].set_teamname(self.team_dict[message.chat.id].get_teamname())
        self.user_dict[message.chat.id].set_role("Scrum Master")  # Scrum Master
        self.bot.send_message(message.chat.id,
                              "Команда \"" + self.team_dict[
                                  message.chat.id].get_teamname() + "\" успешно зарегистрирована!")  # в message.text хранится то, что написал человек
        self.enter_user_name(message)

    def after_product(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        product_name = message.text

        if product_name.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода названия продукта.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        if Team.check_product_for_unique(product_name):
            markup = continue_cancel_buttons()

            msg = self.bot.send_message(message.chat.id,
                                        f"Проверьте правильность ввода\n\n"
                                        f"Название продукта: {product_name}",
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.confirm_enter, self.set_product_name, product_name)
        else:
            self.bot.send_message(message.chat.id, "Такое имя для продукта уже существует")
            self.bot.send_message(message.chat.id, "Пожалуйста, выберите другое имя")
            self.enter_product_name(message)

    def set_report_text(self, message, report):
        departure_time = datetime.now()

        self.report_dict[message.chat.id] = Report()
        self.report_dict[message.chat.id].set_report(report)
        self.report_dict[message.chat.id].set_sprint(int(self.sprint_now[len(self.sprint_now) - 1]))
        self.report_dict[message.chat.id].set_date(departure_time)
        self.report_dict[message.chat.id].set_user(self.user_dict[message.chat.id].get_db_id())

        try:
            self.report_dict[message.chat.id].add_report()

            self.bot.send_message(message.chat.id, "Спасибо за Ваш отчёт!")
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id,
                                  f"Отчет по спринту № {int(self.sprint_now[len(self.sprint_now) - 1])} "
                                  f"уже существует или информация о Вас отсутствует в боте.\n\n"
                                  "Напишите в поддержку (@l1can), чтобы получить помощь!")
            self.start_message(message)

    def report_of_people(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        report = message.text  # в report лежит отчет о проделанной работе
        sprint_num = int(self.sprint_now[len(self.sprint_now) - 1])

        if report.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода текста отчета по спринту № "
                                  f"{sprint_num}.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью"
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        markup = continue_cancel_buttons()

        msg = self.bot.send_message(message.chat.id,
                                    f"Проверьте правильность ввода\n\n"
                                    f"Номер спринта: {sprint_num}\n"
                                    f"Текст отчета: {report}",
                                    reply_markup=markup)

        self.bot.register_next_step_handler(msg, self.confirm_enter, self.set_report_text, report)


bot = StudHelperBot()
bot.start()
