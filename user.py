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
        else:
            self.name = None
            self.surname = None
            self.group = None
            self.username = None
            self.teamname = None
            self.role = None
            self.counter_of_people = 0


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

    def add_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `Пользователи` (`Имя`, `Фамилия`, `Группа`, `User_name`, `Команда`, `Роль`) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.name, self.surname, self.group, self.username, self.teamname,
                                             self.role))  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()
        finally:
            connection.close()

    def delete_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                delete_user = "DELETE FROM `Пользователи` WHERE `User_name` = %s"
                cursor.execute(delete_user, self.username)
                connection.commit()
        finally:
            connection.close()

    def add_name(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Имя` = %s WHERE `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.name, self.username))
                connection.commit()
        finally:
            connection.close()

    def add_surname(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Фамилия` = %s WHERE `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.surname, self.username))
                connection.commit()
        finally:
            connection.close()

    def add_group(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Пользователи` SET `Группа` = %s WHERE `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.group, self.username))
                connection.commit()
        finally:
            connection.close()
    def get_role_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Роль` FROM `Пользователи` WHERE `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.username)
                role = cursor.fetchone()
                connection.commit()
                return role
        finally:
            connection.close()

    def get_teamname_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Команда` FROM `Пользователи` WHERE `User_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.username)
                tmnm = cursor.fetchone()
                connection.commit()
                return tmnm
        finally:
            connection.close()

    def get_name_people_of_team(self): # функция для получения фамилий из бд для определенной группы
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `Фамилия` FROM `Пользователи` WHERE `Команда` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                surnames = cursor.fetchall()
                connection.commit()
                return surnames
        finally:
            connection.close()

    # Метод для проверки наличия пользователя в команде
    def is_in_team(self):
        connection = connect_to_db()
        check = ''
        try:
            with connection.cursor() as cursor:
                user_from_db = "SELECT `Команда` FROM `Пользователи` WHERE `User_name` = %s"
                cursor.execute(user_from_db, self.username)
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
                user_from_db = "SELECT `Администратор` FROM `Команды` WHERE `Администратор` = %s"
                cursor.execute(user_from_db, self.username)
                check = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True
