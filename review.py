from config import host, user, password, db_name
import pymysql.cursors
import datetime


def connect_to_db():
    try:
        connection = pymysql.connect(
            host=host,
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


class Review:

    def __init__(self):
        self.general_mark = None
        self.advtgs = ''
        self.disadvtgs = ''
        self.assessor = None
        self.assessored = None
        self.date = None

    def add_review(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # insert_user = "INSERT INTO `Оценки` (`Общая оценка`, `Решение технических задач`, `Командная работа`, `Ответственность`, `Помощь в решении технических задач`, `User_name`, `Автор отзыва`, `Дата`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                insert_user = "INSERT INTO `team_members_ratings` (`assessor_user_id`, `assessored_user_id`, `overall_rating`, `advantages`, `disadvantages`, `rate_date`) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.assessor, self.assessored, self.general_mark, self.advtgs, self.disadvtgs,
                                             self.date))
                connection.commit()
        finally:
            connection.close()

    def set_assessor(self, db_id):
        self.assessor = db_id

    def set_assessored(self, db_id):
        self.assessored = db_id

    def set_date(self, date):
        self.date = date

    def set_general_mark(self, general_mark):
        self.general_mark = general_mark

    def set_advantages(self, advtgs):
        self.advtgs = advtgs

    def set_disadvantages(self, disadvtgs):
        self.disadvtgs = disadvtgs

    def get_assessor(self):
        return self.assessor

    def get_general_mark(self):
        return self.general_mark

    def get_advantages(self):
        return self.advtgs

    def get_disadvantages(self):
        return self.disadvtgs

    def get_assessored(self):
        return self.assessored

    def get_date(self):
        return self.date
