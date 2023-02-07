import pymysql.cursors
from config import host, user, password, db_name
from user import User


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


class Team:
    # Конструктор
    def __init__(self, *args):
        if len(args) == 2:
            self.teamname = args[0]
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0
            self.team_codes = []
            self.admin_id = args[1]
            self.team_id = None
        else:
            self.teamname = None
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0
            self.team_codes = []
            self.admin_id = 0
            self.team_id = None

    def set_team_id(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `team_id` FROM teams where `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                result = cursor.fetchone()
                connection.commit()
                self.team_id = result['team_id']
        finally:
            connection.close()

    def check_team_with_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # sql_request = "SELECT `Название` FROM `Команды` WHERE `Код` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `user_id` FROM `team_members` WHERE `invite_code` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return True
                return False
        finally:
            connection.close()

    # Метод для вставки новой команды в базу данных
    def add(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "INSERT INTO `Команды` (`Название`, `Администратор`, `Ид`) VALUES (%s, %s, %s)"  # строка для SQL-запроса
                sql_request = "INSERT INTO `teams` (`team_name`, `product_name`, `admin_user_id`) VALUES (%s, %s, %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.teamname, self.product, self.admin_id))
                connection.commit()

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

    # Метод для заполнения поля 'Код команды'
    def add_team_code(self, role, code):  # СЮДА ПЕРЕДАВАЛОСЬ НАЗВАНИЕ КОМАНДЫ, А НУЖНО, ЧТОБЫ ПЕРЕДАВАЛСЯ АЙДИ
        self.set_team_id()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "INSERT INTO `Коды` (`Команда`, `Роль`, `Код`) VALUES (%s, %s, %s)"  # строка для SQL-запроса
                sql_request = "INSERT INTO `team_members` (`team_id`, `role`, `invite_code`) VALUES (%s, %s, %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.team_id, role, code))
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

    """def delete_code_from_bd(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                #sql_request = "DELETE FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                sql_request = "DELETE FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                connection.commit()
        finally:
            connection.close()"""

    @staticmethod
    def get_admin_of_team(code):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT Команда FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                # cursor.execute(sql_request, code)

                # sql_request = "SELECT Ид FROM `Команды` WHERE `Название` = (SELECT Команда FROM `Коды` WHERE `Код` = %s)"  # строка для SQL-запроса
                sql_request = "SELECT `admin_user_id` FROM `teams` WHERE `team_id` IN (SELECT `team_id` FROM `team_members` WHERE `invite_code` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchone()
                connection.commit()
                return result['admin_user_id']
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

    def get_counter_of_people(self):
        return self.counter_of_people

    def set_counter_of_people(self, counter):
        self.counter_of_people = counter

    def set_team_code(self, code):
        self.team_codes.insert(0, code)

    def get_team_code(self):
        return self.team_codes[0]

    def get_admin(self):
        return self.admin_id

    def set_admin(self, admin_id):
        self.admin_id = admin_id
