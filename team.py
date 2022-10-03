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
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0
        else:
            self.teamname = None
            self.admin = None
            self.size_of_team = None
            self.product = None
            self.counter_of_people = 0

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


    def add_product(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `Команды` SET Продукт = (%s) WHERE Название = (%s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.product, self.teamname))
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

    def set_product(self,product):
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
