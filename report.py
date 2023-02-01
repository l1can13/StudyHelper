from config import host, user, password, db_name
import pymysql.cursors

# тупо класс report'ов (отчетов) здесь храним текст отчета, какой спринт, время отправки и дополнительные поля
# ид и юзернейм, чтобы можно было грузить в бд
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


class Report:
    def __init__(self, *args):
        if len(args) == 1:
            self.report = args[0]
        elif len(args) == 2:
            self.report = args[0]
            self.sprint = args[1]

        elif len(args) == 3:
            self.report = args[0]
            self.sprint = args[1]
            self.departure_time = args[2]
        elif len(args) == 4:
            self.report = args[0]
            self.sprint = args[1]
            self.departure_time = args[2]
            self.username = args[3]
        elif len(args) == 5:
            self.report = args[0]
            self.sprint = args[1]
            self.departure_time = args[2]
            self.username = args[3]
            self.id = args[4]
        else:
            self.report = None
            self.sprint = None
            self.departure_time = None

    def set_report(self, report):
        self.report = report

    def set_sprint(self, sprint):
        self.sprint = sprint

    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def set_username(self, username):
        self.username = username

    def set_id(self, id):
        self.id = id

    def get_report(self):
        return self.report

    def get_sprint(self):
        return self.sprint

    def get_departure_time(self):
        return self.departure_time

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def add_report(self): #функция добавления данных в бд
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "INSERT INTO `Отчеты` (`Имя пользователя`, `Автор отчета`, `Текст отчета`, `Дата отправки`, `Спринт`) VALUES (%s, %s, %s, %s, %s);"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.username, self.id, self.report, self.departure_time, self.sprint))
                connection.commit()
        finally:
            connection.close()
