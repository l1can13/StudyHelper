import uuid

import pymysql.cursors
from config import host, user, password, db_name


# Функция для подключения к базе данных
def connect_to_db():
    try:
        connection = pymysql.connect(
            host=host,  # данные берем из файла config (в принципе менять их не нужно)
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected successfully!")
        return connection
    except Exception as ex:
        print("Connection error!", ex)


def create_unique_inv_code():
    return str(uuid.uuid1())[:8]


class Team:
    # Конструктор
    def __init__(self, *args):
        if len(args) == 2:
            self.teamname = args[0]
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0
            self.code = ''
            self.admin_id = args[1]
            self.team_id = None
        else:
            self.teamname = None
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0
            self.code = ''
            self.admin_id = 0
            self.team_id = None

    def get_team_id(self):
        return self.team_id

    def set_team_id_by_db(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `team_id` FROM teams WHERE `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                result = cursor.fetchone()
                connection.commit()
                self.team_id = result['team_id']
        finally:
            connection.close()

    # Метод для вставки новой команды в базу данных
    def add(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "INSERT INTO `teams` (`team_name`, `product_name`, `admin_user_id`, `code`) VALUES (%s, %s, %s, %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.teamname, self.product, self.admin_id, self.code))
                connection.commit()

            self.set_team_id_by_db()
        finally:
            connection.close()

    def find_db_id_by_surname(self, surname):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # sql_request = "SELECT `Ид` FROM `Пользователи` WHERE `Имя` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `user_id` FROM `users` WHERE `name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, surname)
                result = cursor.fetchone()
                connection.commit()
                return result['user_id']
        finally:
            connection.close()

    # Метод для заполнения поля 'Продукты'
    def add_product(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "UPDATE `Команды` SET Продукт = (%s) WHERE Название = (%s)"  # строка для SQL-запроса
                sql_request = "UPDATE `teams` SET `product_name` = (%s) WHERE `team_name` = (%s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.product, self.teamname))
                connection.commit()
        finally:
            connection.close()

    # Метод для удаления определенной команды из базы данных
    def delete(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "DELETE FROM `Команды` WHERE `Название` = %s"  # строка для SQL-запроса
                sql_request = "DELETE FROM `teams` WHERE `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                connection.commit()

                # sql_request = "DELETE FROM `Пользователи` WHERE `Команда` = %s"
                sql_request = "DELETE FROM `team_members` WHERE `team_id` IN (SELECT `team_id` FROM `teams` WHERE `team_name` = %s)"
                cursor.execute(sql_request, self.teamname)
                connection.commit()
        finally:
            connection.close()

    @staticmethod
    def get_count_reviews_every_teammate():
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `users`.`name`, COUNT(`team_members_ratings`.`assessor_user_id`) as count_reviews " \
                              "FROM `users`" \
                              "LEFT JOIN `team_members_ratings` " \
                              "ON `users`.`user_id` = `team_members_ratings`.`assessor_user_id` " \
                              "GROUP BY `users`.`user_id`"  # строка для SQL-запроса
                cursor.execute(sql_request)
                result = cursor.fetchall()
                connection.commit()

                return result
        finally:
            connection.close()

    @staticmethod
    def get_count_reports_every_teammate():
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `users`.`name`, COUNT(`sprint_reports`.`user_id`) as count_reports " \
                              "FROM `users`" \
                              "LEFT JOIN `sprint_reports` " \
                              "ON `users`.`user_id` = `sprint_reports`.`user_id` " \
                              "GROUP BY `users`.`user_id`"  # строка для SQL-запроса
                cursor.execute(sql_request)
                result = cursor.fetchall()
                connection.commit()

                return result
        finally:
            connection.close()

    @staticmethod
    def check_teamname_for_unique(teamname):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT * FROM `Команды` WHERE `Название` = %s"  # строка для SQL-запроса
                sql_request = "SELECT * FROM `teams` WHERE `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, teamname)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return False
                return True
        finally:
            connection.close()

    @staticmethod
    def check_product_for_unique(
            product):  # вернет true если в бд ничего нет (то есть уникальное название) и false, если такое уже есть
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT * FROM `Команды` WHERE `Продукт` = %s"  # строка для SQL-запроса
                sql_request = "SELECT * FROM `teams` WHERE `product_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, product)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return False
                return True
        finally:
            connection.close()

    @staticmethod
    def get_teamname_by_code(code):
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `team_name` FROM `teams` " \
                              "WHERE `code` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchone()
                connection.commit()

                return result['team_name'] if result is not None else None
        finally:
            connection.close()

    @staticmethod
    def get_team_id_by_teamname(teamname):
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `team_id` FROM `teams` " \
                              "WHERE `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, teamname)
                result = cursor.fetchone()
                connection.commit()

                return result['team_id'] if result is not None else -1
        finally:
            connection.close()

    # Getters/Setters
    def set_teamname(self, teamname):
        self.teamname = teamname

    def get_teamname(self):
        return self.teamname

    def set_product(self, product):
        self.product = product

    def get_product(self):
        return self.product

    def get_size_of_team(self):
        return self.size_of_team

    def set_size_of_team(self, size):
        self.size_of_team = size

    def set_team_id(self, team_id):
        self.team_id = team_id

    def get_counter_of_people(self):
        return self.counter_of_people

    def set_counter_of_people(self, counter):
        self.counter_of_people = counter

    def set_team_code(self, code):
        self.code = code

    def create_team_code(self):
        self.code = create_unique_inv_code()

    def get_team_code(self):
        return self.code

    def get_admin(self):
        return self.admin_id

    def set_admin(self, admin_id):
        self.admin_id = admin_id

    @staticmethod
    def get_team_from_db(tg_id):
        # self.teamname = None +
        # self.product = None +
        # self.code = '' +
        # self.admin_id = 0 +
        # self.team_id = None +

        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                sql_request = (
                    "SELECT `teams`.`team_id`, `teams`.team_name, `teams`.product_name, `teams`.admin_user_id, `teams`.code "
                    "FROM `teams` "
                    "LEFT JOIN `team_members` ON `teams`.team_id = `team_members`.team_id "
                    "LEFT JOIN `users` ON `team_members`.user_id = `users`.user_id "
                    "WHERE `users`.`tg_id` = %s")
                cursor.execute(sql_request, tg_id)

                result = cursor.fetchone()

                if result is None:
                    return Team()

                team_result = Team()

                team_result.set_team_id(result['team_id'])
                team_result.set_teamname(result['team_name'])
                team_result.set_product(result['product_name'])
                team_result.set_admin(result['admin_user_id'])
                team_result.set_team_code(result['code'])

                return team_result
        finally:
            connection.close()
