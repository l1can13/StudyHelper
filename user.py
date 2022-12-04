from config import host, user, password, db_name
import pymysql.cursors


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


class User:
    def __init__(self, *args):
        if len(args) == 1:
            self.name = args[0]
            self.counter_of_people = 0
        elif len(args) == 2:
            self.name = args[0]
            self.surname = args[1]
            self.counter_of_people = 0
        elif len(args) == 3:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.counter_of_people = 0
        elif len(args) == 4:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.counter_of_people = 0
        elif len(args) == 5:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.counter_of_people = 0
        elif len(args) == 6:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.role = args[5]
            self.counter_of_people = 0
        elif len(args) == 7:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.role = args[5]
            self.id = args[6]
            self.counter_of_people = 0

        else:
            self.name = None
            self.surname = None
            self.group = None
            self.username = None
            self.teamname = None
            self.role = None
            self.id = 0
            self.counter_of_people = 0
        self.report = None
        self.departure_time = None

    def find_username_by_surname(self, surname):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `Ид` FROM `Пользователи` WHERE `Имя` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, surname)
                result = cursor.fetchone()
                connection.commit()
                return result['Ид']
        finally:
            connection.close()

    def get_counter_of_people(self):
        return self.counter_of_people

    def set_counter_of_people(self, counter):
        self.counter_of_people = counter

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_surname(self, surname):
        self.surname = surname

    def get_surname(self):
        return self.surname

    def set_group(self, group):
        self.group = group

    def get_group(self):
        return self.group

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_teamname(self, teamname):
        self.teamname = teamname

    def get_teamname(self):
        return self.teamname

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def set_id(self, arg):
        self.id = arg

    def get_id(self):
        return self.id

    def get_report(self):
        return  self.report

    def set_report(self,arg):
        self.report = arg

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, arg):
        self.departure_time = arg

    def add_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `Пользователи` (`Имя`, `Группа`, `User_name`, `Команда`, `Роль`, `Ид`) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.name, self.group, self.username, self.teamname,
                                             self.role, self.id))  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()
        finally:
            connection.close()

    def delete_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                delete_user = "DELETE FROM `Пользователи` WHERE `Ид` = %s"
                cursor.execute(delete_user, self.id)
                connection.commit()
        finally:
            connection.close()

    def add_name(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Имя` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.name, self.id))
                connection.commit()
        finally:
            connection.close()

    def add_username(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `User_name` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.username, self.id))
                connection.commit()
        finally:
            connection.close()

    def add_surname(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Фамилия` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.surname, self.id))
                connection.commit()
        finally:
            connection.close()

    def add_group(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Группа` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.group, self.id))
                connection.commit()
        finally:
            connection.close()

    def get_role_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Роль` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.id, self.username))
                role = cursor.fetchone()
                connection.commit()
                return role['Роль']
        finally:
            connection.close()

    def get_teamname_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Команда` FROM `Пользователи` WHERE `Ид` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.id)
                tmnm = cursor.fetchone()
                connection.commit()
                return tmnm['Команда']
        finally:
            connection.close()

    # Метод для проверки наличия пользователя в команде
    def is_in_team(self):
        connection = connect_to_db()
        check = ''
        try:
            with connection.cursor() as cursor:
                user_from_db = "SELECT `Команда` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"
                cursor.execute(user_from_db, (self.id, self.username))
                check = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True

    def is_admin(self):
        connection = connect_to_db()
        check = ''
        try:
            with connection.cursor() as cursor:
                user_from_db = "SELECT `Название` FROM `Команды` WHERE `Ид` = %s"
                cursor.execute(user_from_db, self.id)
                check = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True

    def check_team_with_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `Команда` FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return True
                return False
        finally:
            connection.close()

    def get_team_using_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `Команда` FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                for row in result:
                    return row['Команда']
        finally:
            connection.close()


    def get_role_using_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `Роль` FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                for row in result:
                    return row['Роль']
        finally:
            connection.close()

    def update_id_in_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Ид` = %s WHERE `Команда` = %s AND `Роль` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.id, self.teamname, self.role))
                connection.commit()
        finally:
            connection.close()

    def get_name_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Имя` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.id, self.username))
                role = cursor.fetchone()
                connection.commit()
                return role['Имя']
        finally:
            connection.close()


    def add_report(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "INSERT INTO `Отчеты` (`Имя пользователя`, `Автор отчета`, `Текст отчета`, `Дата отправки`) VALUES (%s, %s, %s, %s);"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.username, self.id, self.report, self.departure_time))
                connection.commit()
        finally:
            connection.close()