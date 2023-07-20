from config import host, user, password, db_name
import pymysql.cursors
import datetime


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
    def __init__(self):
        self.report = ''
        self.sprint = None
        self.db_id = None
        self.date = None

    def set_report(self, report):
        self.report = report

    def set_sprint(self, sprint):
        self.sprint = sprint

    def set_date(self, date):
        self.date = date

    def set_user(self, user):
        self.db_id = user

    def get_report(self):
        return self.report

    def get_sprint(self):
        return self.sprint

    def get_date(self):
        return self.date

    def get_user(self):
        return self.db_id

    def add_report(self):  # функция добавления данных в бд
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "INSERT INTO `Отчеты` (`Имя пользователя`, `Автор отчета`, `Текст отчета`, `Дата отправки`, `Спринт`) VALUES (%s, %s, %s, %s, %s);"  # строка для SQL-запроса
                sql_request = "INSERT INTO `sprint_reports` (`user_id`, `sprint_num`, `report_text`, `report_date`) VALUES (%s, %s, %s, %s);"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.db_id, self.sprint, self.report, self.date))
                connection.commit()
        finally:
            connection.close()

    def update_report(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `sprint_reports`" \
                              "SET `report_text` = %s," \
                              "`report_date` = %s" \
                              "WHERE `user_id` = %s and `sprint_num` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.report, self.date, self.db_id, self.sprint))
                connection.commit()
        finally:
            connection.close()
