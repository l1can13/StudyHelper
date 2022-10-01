from config import host, user, password, db_name
import pymysql.cursors

def connect_to_db():
    try:
        connection = pymysql.connect(
            host=host, # данные берем из файла config (в принципе менять их не нужно)
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
        elif len(args) == 2:
            self.name = args[0]
            self.surname = args[1]
        elif len(args) == 3:
            self.name = args[0]
            self.surname = args[1]
            self.username = args[2]
        elif len(args) == 4:
            self.name = args[0]
            self.surname = args[1]
            self.username = args[2]
            self.teamname = args[3]
        elif len(args) == 5:
            self.name = args[0]
            self.surname = args[1]
            self.username = args[2]
            self.teamname = args[3]
            self.role = args[4]
        else:
            self.name = None
            self.surname = None
            self.username = None
            self.teamname = None
            self.role = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_surname(self, surname):
        self.surname = surname

    def get_surname(self):
        return self.surname

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
                insert_user = "INSERT INTO `Пользователи` (`Имя`, `Фамилия`, `User_name`, `Команда`, `Роль`) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.name, self.surname, self.username, self.teamname, self.role)) # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
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

    # Метод для проверки наличия пользователя в команде
    def is_in_team(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                user_from_db = "SELECT `Команда` FROM `Пользователи` WHERE `User_name` = %s"
                cursor.execute(user_from_db, self.username)
                connection.commit()
        finally:
            connection.close()

        if user_from_db != "":
            return True
        return False
