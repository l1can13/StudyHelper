from datetime import datetime

import telebot
from pymysql import IntegrityError
from telebot import types
from telebot.types import ReplyKeyboardRemove

from report import Report
from team import Team
from user import User


def continue_cancel_buttons(button1='Продолжить', button2='Изменить'):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton(button1)
    item2 = types.KeyboardButton(button2)
    item3 = types.KeyboardButton("Отмена")
    markup.row(item1, item2)
    markup.add(item3)

    return markup


class StudHelperBot:

    def __init__(self):
        self.token = "..."  # prod
        # self.token = "..."  # dev
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
        try:
            self.user_dict[message.chat.id] = User.get_user_from_db(message.chat.id)

            self.team_dict[message.chat.id] = Team.get_team_from_db(message.chat.id)
        except TypeError:
            self.team_dict[message.chat.id] = Team(None, None)

        self.tg_name_of_user_dict[message.chat.id] = ''
        self.first_hello_dict[message.chat.id] = self.user_dict[message.chat.id].is_in_team()

    def start(self):
        self.bot.infinity_polling()

    def start_message(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        if message.text.startswith('/start ') and message.text != 'Отмена регистрации':
            message.text = message.text.split()[1]
            self.accept_invitation(message)
        else:
            if self.user_dict[message.chat.id].is_admin():
                buttons = [
                    types.KeyboardButton("Ссылка-приглашение"),
                    types.KeyboardButton("Удалить участника"),
                    types.KeyboardButton("Моя команда"),
                    types.KeyboardButton("Мои отчёты"),
                    types.KeyboardButton("Отправить отчёт"),
                    types.KeyboardButton("Удалить отчёт"),
                    types.KeyboardButton("Помощь"),
                    types.KeyboardButton("Отчёт о команде"),
                ]

                rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

                for row in rows:
                    markup.row(*row)
            elif self.user_dict[message.chat.id].is_in_team():
                if self.user_dict[message.chat.id].get_teamname() is None:
                    self.user_dict[message.chat.id].set_teamname(self.user_dict[message.chat.id].get_teamname_from_bd())

                if self.user_dict[message.chat.id].get_role() is None:
                    self.user_dict[message.chat.id].set_role(self.user_dict[message.chat.id].get_role_from_bd())

                if self.user_dict[message.chat.id].get_name() is None:
                    self.user_dict[message.chat.id].set_name(self.user_dict[message.chat.id].get_name_from_bd())

                if self.user_dict[message.chat.id].get_name() is None:
                    msg = self.bot.send_message(message.chat.id, "Введите Ваше имя и фамилию:")
                    self.bot.register_next_step_handler(msg, self.after_name)
                    return
                else:
                    buttons = [
                        types.KeyboardButton("Моя команда"),
                        types.KeyboardButton("Мои отчёты"),
                        types.KeyboardButton("Отправить отчёт"),
                        types.KeyboardButton("Удалить отчёт"),
                        types.KeyboardButton("Помощь"),
                    ]

                    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

                    for row in rows:
                        markup.row(*row)
            else:
                item1 = types.KeyboardButton("Регистрация команды")
                item5 = types.KeyboardButton("Помощь")
                markup.add(item1)
                markup.add(item5)
            try:
                if not self.first_hello_dict[message.chat.id]:
                    if self.user_dict[message.chat.id].get_username() is not None:
                        self.bot.send_message(message.chat.id,
                                              "Привет, " + self.user_dict[message.chat.id].get_username(),
                                              reply_markup=markup)
                    else:
                        self.bot.send_message(message.chat.id, "Привет!", reply_markup=markup)
                    self.first_hello_dict[message.chat.id] = True
                else:
                    self.bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=markup)
            except KeyError:
                self.bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=markup)

    def message_reply(self, message):
        if message.text == "Регистрация команды":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Отмена регистрации")
            item2 = types.KeyboardButton("Продолжить регистрацию")
            markup.add(item1, item2)
            msg = self.bot.send_message(message.chat.id,
                                        "Внимание! Команду должен регистрировать Scrum Master! Если Вы не являетесь "
                                        "Scrum Master'ом, то нажмите кнопку 'Отмена регистрации'. Если являетесь - "
                                        "нажмите кнопку 'Продолжить регистрацию'",
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.continue_registration)
        elif message.text == "Помощь":
            self.bot.send_message(
                message.chat.id,
                "Возникла проблема с ботом, или нашли баг?\n\nНапишите @l1can для получения "
                "информации по боту, а также для решения любой проблемы (как создать команду, "
                "переименование/удаление команды, удаление участников, "
                "переименование/удаление продукта, и т.д)\n\n"
                "Инструкция по боту находится по адресу: studhelper.online/faq"
            )
            self.start_message(message)
        elif message.text == "Ссылка-приглашение":
            self.generate_or_get_team_code(message)
        elif message.text == "Отправить отчёт":
            self.choose_sprint_on_review(message)
        elif message.text.lower() == "обновить":
            self.bot.send_message(message.chat.id, "Обновляю состояние бота...",
                                  reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Моя команда":
            self.team_information(message)
        elif message.text == "Мои отчёты":
            self.my_reports(message)
        elif message.text == "Удалить отчёт":
            self.number_selection(message)
        elif message.text == "Отчёт о команде":
            self.get_team_report(message)
        elif message.text == "Удалить участника":
            self.teammate_selection(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.start_message(message)

    def continue_registration(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        if message.text == "Отмена регистрации":
            self.bot.send_message(message.chat.id, "Возврат к главному меню", reply_markup=ReplyKeyboardRemove())
            self.start_message(message)
        elif message.text == "Продолжить регистрацию":
            self.team_registration(message)

    def teammate_selection(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        if not self.user_dict[message.chat.id].is_admin():
            self.bot.send_message(message.chat.id, "У Вас нет прав, чтобы отправить данную команду!")
            self.start_message(message)
            return

        markup = self.get_teammates_markup(message)

        if markup is None:
            self.bot.send_message(message.chat.id,
                                  "В Вашей команде нет людей кроме Вас.",
                                  reply_markup=markup,
                                  parse_mode="Markdown")
            self.start_message(message)
            return

        msg = self.bot.send_message(message.chat.id,
                                    "С помощью меню кнопок выберите кого Вы хотите удалить из команды",
                                    reply_markup=markup,
                                    parse_mode="Markdown")

        self.bot.register_next_step_handler(msg, self.confirm_delete_teammate)

    def confirm_delete_teammate(self, message):
        if message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        elif message.text.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе удаления члена команды.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return
        elif message.text in self.get_teammates_list(message):
            teammate = message.text

            markup = continue_cancel_buttons('Да', 'Нет')

            msg = self.bot.send_message(message.chat.id,
                                        f'Вы уверены, что хотите удалить этого члена команды: {teammate}?',
                                        reply_markup=markup,
                                        parse_mode="Markdown")

            self.bot.register_next_step_handler(msg, self.delete_teammate, teammate)
        else:
            self.bot.send_message(message.chat.id, "Выберите члена команды из предложенных в меню кнопок!")
            self.number_selection(message)

    def delete_teammate(self, message, teammate):
        if message.text == 'Нет':
            self.bot.send_message(message.chat.id, "Возвращаюсь в меню выбора члена команды...")
            self.teammate_selection(message)
            return
        elif message.text == 'Да':
            try:
                deleted_user_id = User.get_id_by_name(teammate)
                deleted_tg_id = User.get_tg_id_by_user_id(deleted_user_id)

                User.delete_user_from_team(deleted_user_id)

                self.bot.send_message(message.chat.id, f"Пользователь {teammate} успешно удалён! Возвращаюсь в "
                                                       "основное меню...")

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Регистрация команды")
                item5 = types.KeyboardButton("Помощь")
                markup.add(item1)
                markup.add(item5)

                self.first_hello_dict[deleted_tg_id] = False

                self.bot.send_message(deleted_tg_id, "*Вас удалили из команды!*\n"
                                                     "Если Вы хотите присоединиться к другой команде - попросите "
                                                     "Scrum-мастера ссылку-приглашение и перейдите по ней.\n\n"
                                                     "Для создания своей команды - воспользуйтесь кнопкой "
                                                     "\"Регистрация команды\".",
                                      reply_markup=markup,
                                      parse_mode='Markdown')

                self.start_message(message)
            except IntegrityError:
                self.bot.send_message(message.chat.id,
                                      "Информация о данном члене команды не найдена! Возвращаюсь в основное меню...")
                self.start_message(message)
        elif message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(")
            self.start_message(message)

    def get_team_report(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        try:
            if not self.user_dict[message.chat.id].is_admin():
                self.bot.send_message(message.chat.id, "У Вас нет прав, чтобы отправить данную команду!")
                self.start_message(message)
                return

            reviews_list = self.team_dict[message.chat.id].get_count_reviews_every_teammate()
            reviews_str = '\n'.join([f"{review['name']} - {review['count_reviews']}"
                                     for review in reviews_list])

            reports_list = self.team_dict[message.chat.id].get_count_reports_every_teammate()
            reports_str = '\n'.join([f"{report['name']} - {report['count_reports']}"
                                     for report in reports_list])

            reviews_normal = self.user_dict[message.chat.id].get_count_teammates()
            reports_normal = 6

            self.bot.send_message(message.chat.id,
                                  f"*Отчет о команде\n\n*"
                                  f"*Количество авторства оценок (сколько каждый член команды поставил оценок другим "
                                  f"членам команды)*\n"
                                  f"{reviews_str}\n\n"
                                  f"*Количество отчётов*\n"
                                  f"{reports_str}\n\n"
                                  f"Должно быть отзывов о членах команды: *{reviews_normal['count_teammates']}*\n"
                                  f"Должно быть отчетов о проделанной работе: *{reports_normal}*",
                                  parse_mode='Markdown')
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вас отсутствует в боте!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def get_reports_str(self, message):
        reports_list = self.user_dict[message.chat.id].get_reports()
        reports_str = \
            '\n'.join([f"*Спринт №{report['sprint_num']}*\n"
                       f"Дата отправки: {report['report_date']}\n\n"
                       f"Текст отчёта:\n{report['report_text']}\n"
                       f"\n----------------------------------------\n"
                       for report in reports_list]) \
                if reports_list \
                else 'У Вас нет отчётов.'

        return reports_str

    def get_sprint_numbers_list(self, message):
        return [''.join(f"Спринт №{report['sprint_num']}") for report in self.user_dict[message.chat.id].get_reports()]

    def get_sprint_numbers_markup(self, message):
        reports_list = self.user_dict[message.chat.id].get_reports()
        sprint_numbers = [report['sprint_num'] for report in reports_list]
        cancel = types.KeyboardButton("Отмена")

        if sprint_numbers:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for sprint_num in sprint_numbers:
                button = types.KeyboardButton(f"Спринт №{sprint_num}")
                markup.add(button)
            markup.add(cancel)
        else:
            markup = None

        return markup

    def get_teammates_markup(self, message):
        teammates = [teammate for teammate in self.user_dict[message.chat.id].get_teammates_excludes_me() if
                     teammate['name'] != 'invited_user']

        cancel = types.KeyboardButton("Отмена")

        if teammates:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for teammate in teammates:
                button = types.KeyboardButton(f"{teammate['name']}")
                markup.add(button)
            markup.add(cancel)
        else:
            markup = None

        return markup

    def get_teammates_list(self, message):
        teammates_list = self.user_dict[message.chat.id].get_teammates_excludes_me()
        return [teammate['name'] for teammate in teammates_list if teammate['name'] != 'invited_user']

    def number_selection(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        reports_str = self.get_reports_str(message)

        self.bot.send_message(message.chat.id,
                              reports_str,
                              parse_mode="Markdown")

        if reports_str == "У Вас нет отчётов.":
            self.start_message(message)
            return

        markup = self.get_sprint_numbers_markup(message)

        msg = self.bot.send_message(message.chat.id,
                                    'Какой отчёт вы хотите удалить?\n\n'
                                    '*Выберите спринт из списка*',
                                    reply_markup=markup,
                                    parse_mode="Markdown")

        self.bot.register_next_step_handler(msg, self.confirm_delete_report)

    def confirm_delete_report(self, message):
        if len(message.text) == 0:
            self.bot.send_message(message.chat.id, "Выберите спринт из предложенных в меню кнопок!")
            self.number_selection(message)
        if message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        elif message.text.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе выбора спринта для удаления.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return
        elif message.text in self.get_sprint_numbers_list(message):
            sprint_num = message.text

            markup = continue_cancel_buttons('Да', 'Нет')

            msg = self.bot.send_message(message.chat.id,
                                        f'Вы уверены, что хотите удалить отчёт по *спринту № {sprint_num[-1]}*?',
                                        reply_markup=markup,
                                        parse_mode="Markdown")

            self.bot.register_next_step_handler(msg, self.delete_report, sprint_num)
        else:
            self.bot.send_message(message.chat.id, "Выберите спринт из предложенных в меню кнопок!")
            self.number_selection(message)

    def delete_report(self, message, sprint_num):
        if message.text == 'Нет':
            self.bot.send_message(message.chat.id, "Возвращаюсь в меню выбора спринта...")
            self.number_selection(message)
            return
        elif message.text == 'Да':
            try:
                self.report_dict[message.chat.id] = Report()
                self.report_dict[message.chat.id].set_sprint(sprint_num[-1])
                self.report_dict[message.chat.id].set_user(self.user_dict[message.chat.id].get_db_id())

                self.report_dict[message.chat.id].delete_report()

                self.bot.send_message(message.chat.id, "Отчет успешно удален! Возвращаюсь в основное меню...")
                self.start_message(message)
            except IntegrityError:
                self.bot.send_message(message.chat.id,
                                      "Информация об отчете не найдена! Возвращаюсь в основное меню...")
                self.start_message(message)
        elif message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.start_message(message)

    def my_reports(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        try:
            self.bot.send_message(message.chat.id,
                                  self.get_reports_str(message),
                                  parse_mode="Markdown")
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вас отсутствует в боте!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def team_information(self, message):
        if message.chat.id not in self.user_dict or message.chat.id not in self.team_dict:
            self.update(message)

        try:
            team_name = self.user_dict[message.chat.id].get_teamname() \
                if self.user_dict[message.chat.id].get_teamname() is not None \
                else self.user_dict[message.chat.id].get_teamname_from_bd()

            product = self.team_dict[message.chat.id].get_product() \
                if self.team_dict[message.chat.id].get_product() is not None \
                else self.user_dict[message.chat.id].get_product_from_db()

            teammates_list = [teammate for teammate in self.user_dict[message.chat.id].get_teammates() if
                              teammate['name'] != 'invited_user']
            teammates_str = '\n'.join([f"{teammate['name']} - {teammate['role']}" for teammate in teammates_list])

            self.bot.send_message(message.chat.id,
                                  f"Название команды: {team_name}\n"
                                  f"Продукт: {product}\n\n"
                                  f"Члены команды:\n{teammates_str}")
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вашей команде отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def team_registration(self, message):
        self.bot.send_message(message.chat.id, "Заполните форму ниже", reply_markup=ReplyKeyboardRemove())
        msg = self.bot.send_message(message.chat.id, "Введите название команды: ")
        self.bot.register_next_step_handler(msg, self.enter_team_name)

    def choose_sprint_on_review(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        buttons = [types.KeyboardButton(sprint) for sprint in self.sprints]
        cancel_button = types.KeyboardButton('Отмена')

        markup.row(buttons[0], buttons[3])
        markup.row(buttons[1], buttons[4])
        markup.row(buttons[2], buttons[5])
        markup.add(cancel_button)

        msg = self.bot.send_message(message.chat.id, "Выберите спринт: ",
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
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
                                  "к технической поддержке (@l1can).")
            self.start_message(message)
            return

        if message.text in self.sprints:
            self.sprint_now = message.text  # будет в формате "Спринт №1"/"Спринт №2" и тд
            msg = self.bot.send_message(
                message.chat.id, "Напишите текст вашего отчета.\n\n"
                                 "*Минимальное количество символов* - 30.\n"
                                 "*Максимальное количество символов* - 600.\n"
                                 "Формат: *1 строка - 1 задача.*",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='Markdown'
            )
            self.bot.register_next_step_handler(msg, self.report_of_people)
        elif message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(", reply_markup=ReplyKeyboardRemove())
            self.choose_sprint_on_review(message)

    def generate_or_get_team_code(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        if not self.user_dict[message.chat.id].is_admin():
            self.bot.send_message(message.chat.id, "У Вас нет прав, чтобы отправить данную команду!")
            self.start_message(message)
            return

        try:
            team_code = self.user_dict[message.chat.id].get_team_code()

            if team_code is not None:
                self.bot.send_message(
                    message.chat.id,
                    "Ссылка приглашение в вашу команду (отправьте ее участникам команды, чтобы они могли "
                    "присоединиться):"
                )
                # self.bot.send_message(message.chat.id, f"https://t.me/StudHelperDevBot?start={team_code}")  # dev
                self.bot.send_message(message.chat.id, f"https://t.me/Helping_Student_bot?start={team_code}")  # prod
                self.start_message(message)
                return
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вашей команде отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def add_user_to_bd(self, message):
        if message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
            return
        elif message.text not in self.roles:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :( ")
            self.generate_or_get_team_code(message)
            return

        try:
            self.user_dict[message.chat.id].set_role(message.text)
            self.user_dict[message.chat.id].add_user_to_team_members()

            self.bot.send_message(message.chat.id, "Ваши данные успешно сохранены!")
            self.start_message(message)
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вашей команде отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
            self.start_message(message)

    def accept_invitation(self, message):
        try:
            if message.chat.id not in self.user_dict:
                self.update(message)

            if self.user_dict[message.chat.id].is_in_team():
                self.bot.send_message(message.chat.id, "Вы уже находитесь в команде!")
                self.start_message(message)
                return

            teamname = Team.get_teamname_by_code(message.text)
            if teamname is not None:
                if self.user_dict[message.chat.id].is_exists():
                    self.user_dict[message.chat.id].set_teamname(teamname)
                    self.user_dict[message.chat.id].set_team_id(Team.get_team_id_by_teamname(teamname))

                    self.bot.send_message(
                        message.chat.id,
                        f"Информация о Вас найдена! Вы успешно добавлены в команду \"{teamname}\"!"
                    )

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                    buttons = [types.KeyboardButton(role) for role in self.roles]
                    cancel_button = types.KeyboardButton('Отмена')

                    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
                    for row in rows:
                        markup.row(*row)

                    markup.add(cancel_button)

                    msg = self.bot.send_message(
                        message.chat.id,
                        "Выберите свою роль: ",
                        reply_markup=markup
                    )
                    self.bot.register_next_step_handler(msg, self.add_user_to_bd)
                    return

                self.user_dict[message.chat.id].set_team_id(Team.get_team_id_by_teamname(teamname))

                self.bot.send_message(message.chat.id, f"Вы успешно добавлены в команду \"{teamname}\"!")
                self.enter_user_name(message)
                return
            else:
                self.bot.send_message(message.chat.id, "Команда с такой ссылкой-приглашением не найдена!")
                self.start_message(message)
                return
        except IntegrityError:
            self.bot.send_message(message.chat.id, "Кажется, информация о Вашей команде отсутствует!\n\n"
                                                   "Напишите в поддержку (@l1can), чтобы получить помощь!\n\n")
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
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
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
                                        f"Проверьте правильность ввода. Формат должен быть таким: Фамилия Имя\n\n"
                                        f"Ваше Фамилия Имя:\n{name}",
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
            self.user_dict[message.chat.id].add()

            if self.user_dict[message.chat.id].get_team_id() is None:
                self.team_dict[message.chat.id].create_team_code()
                self.team_dict[message.chat.id].set_admin(self.user_dict[message.chat.id].get_db_id())
                self.team_dict[message.chat.id].add()
                self.user_dict[message.chat.id].set_team_id(self.team_dict[message.chat.id].get_team_id())
                self.user_dict[message.chat.id].add_user_to_team_members()
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                buttons = [types.KeyboardButton(role) for role in self.roles]
                cancel_button = types.KeyboardButton('Отмена')

                rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
                for row in rows:
                    markup.row(*row)

                markup.add(cancel_button)

                msg = self.bot.send_message(
                    message.chat.id,
                    "Выберите свою роль: ",
                    reply_markup=markup
                )
                self.bot.register_next_step_handler(msg, self.add_user_to_bd)
                return

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
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
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
        elif message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(. Попробуйте снова.")
            edit(message)

    def enter_team_name(self,
                        message):  # функция, где запрашивается название продукта и сохраняется в бд имя команды
        if message.chat.id not in self.user_dict:
            self.update(message)

        name_of_team = message.text

        if name_of_team.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода названия команды.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
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
        msg = self.bot.send_message(message.chat.id, "Введите название продукта: ",
                                    reply_markup=ReplyKeyboardRemove())
        self.bot.register_next_step_handler(msg, self.after_product)

    def set_product_name(self, message, product_name):
        if message.chat.id not in self.user_dict:
            self.update(message)

        self.team_dict[message.chat.id].set_product(product_name)

        self.user_dict[message.chat.id].set_teamname(self.team_dict[message.chat.id].get_teamname())
        self.user_dict[message.chat.id].set_role("Scrum Master")  # Scrum Master
        self.bot.send_message(message.chat.id,
                              "Команда \"" + self.team_dict[
                                  message.chat.id].get_teamname() + "\" успешно зарегистрирована!")  # в message.text хранится то, что написал человек

        if self.user_dict[message.chat.id].is_exists():
            markup = continue_cancel_buttons()

            msg = self.bot.send_message(message.chat.id,
                                        f"Информация о Вас найдена, проверьте её правильность\n\n"
                                        f"Ваше имя: {self.user_dict[message.chat.id].get_name_from_db()}\n"
                                        f"Ваша группа: {self.user_dict[message.chat.id].get_group_from_db()}",
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.confirm_existed_user_info)
        else:
            self.enter_user_name(message)

    def confirm_existed_user_info(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        if message.text == 'Изменить':
            self.enter_user_name(message)
            return
        elif message.text == 'Продолжить':
            self.start_message(message)
            return
        elif message.text == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)

    def after_product(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        product_name = message.text

        if product_name.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода названия продукта.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
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

    def rewrite_report(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        answer = message.text

        if answer == 'Да':
            self.report_dict[message.chat.id].update_report()

            self.bot.send_message(message.chat.id, "Отчет успешно обновлен. Возвращаюсь в основное меню...")
            self.start_message(message)
        elif answer == 'Нет':
            self.bot.send_message(message.chat.id, "Возвращаюсь в основное меню...")
            self.start_message(message)
        elif answer == 'Отмена':
            self.bot.send_message(message.chat.id, "Отменяю действие и возвращаюсь в основное меню...")
            self.start_message(message)
        else:
            self.bot.send_message(message.chat.id, "Я вас не понимаю :(")
            self.start_message(message)

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
            markup = continue_cancel_buttons('Да', 'Нет')

            msg = self.bot.send_message(message.chat.id,
                                        f"Отчет по спринту № {int(self.sprint_now[len(self.sprint_now) - 1])} "
                                        f"уже существует.\n\n"
                                        f"*Хотите перезаписать данный отчет?*\n\n",
                                        parse_mode='Markdown',
                                        reply_markup=markup)

            self.bot.register_next_step_handler(msg, self.rewrite_report)

    def report_of_people(self, message):
        if message.chat.id not in self.user_dict:
            self.update(message)

        report = message.text  # в report лежит отчет о проделанной работе

        if len(report) < 30:
            self.bot.send_message(message.chat.id,
                                  "Минимальная длина отчета - 30 символов!\n"
                                  "Пожалуйста, отправьте отчёт снова.")
            self.start_message(message)
            return
        elif len(report) > 600:
            self.bot.send_message(message.chat.id,
                                  "Максимальная длина отчета - 500 символов!\n"
                                  "Пожалуйста, отправьте отчёт снова.")
            self.start_message(message)

        sprint_num = int(self.sprint_now[len(self.sprint_now) - 1])

        if report.startswith('/start'):
            self.bot.send_message(message.chat.id,
                                  "Вы пытаетесь начать общение с ботом или ввести ссылку-приглашение "
                                  "в процессе ввода текста отчета по спринту № "
                                  f"{sprint_num}.\n\n"
                                  "Начните процесс заново "
                                  "(если Вы начинали делать это ранее) или обратитесь за помощью "
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
