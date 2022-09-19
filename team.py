import pymysql.cursors
from config import host, user, password, db_name


# Функция для подключения к базе данных
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


class Team:
    # Конструктор
    def __init__(self, *args):
        if len(args) == 2:
            self.teamname = args[0]
            self.admin = args[1]
        else:
            self.teamname = None
            self.admin = None

    # Метод для вставки новой команды в базу данных
    def add(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "INSERT INTO `Команды` (`Название`, `Администратор`) VALUES (%s, %s)" # строка для SQL-запроса
                cursor.execute(sql_request, (self.teamname, self.admin))
                connection.commit()
        finally:
            connection.close()

    # Метод для удаления определенной команды из базы данных
    def delete(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "DELETE FROM `Команды` WHERE `Название` = %s" # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                connection.commit()
        finally:
            connection.close()

    # Getters/Setters
    def set_admin(self, admin):
        self.admin = admin

    def get_admin(self):
        return self.admin

    def set_name(self, teamname):
        self.teamname = teamname

    def get_name(self):
        return self.teamname
