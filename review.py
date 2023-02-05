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
        self.user = None
        self.reviewer = None
        self.date = None

    def add_review(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                #insert_user = "INSERT INTO `Оценки` (`Общая оценка`, `Решение технических задач`, `Командная работа`, `Ответственность`, `Помощь в решении технических задач`, `User_name`, `Автор отзыва`, `Дата`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                insert_user = "INSERT INTO `team_members_ratings` (`assessor_user_id`, `assessored_user_id`, `overall_rating`, `advantages`, `disadvantages`, `rate_date`) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.reviewer, self.user, self.general_mark, self.advtgs, self.disadvtgs, self.date))
                connection.commit()
        finally:
            connection.close()

    def set_user(self, username):
        self.user = username

    def set_reviewer(self, reviewer):
        self.reviewer = reviewer

    def set_date(self, date):
        self.date = date

    def set_general_mark(self, general_mark):
        self.general_mark = general_mark

    def set_advtgs(self, advtgs):
        self.advtgs = advtgs

    def set_disadvtgs(self, disadvtgs):
        self.disadvtgs = disadvtgs

    def get_user(self):
        return self.user

    def get_general_mark(self):
        return self.general_mark

    def get_advtgs(self):
        return self.advtgs

    def get_disadvtgs(self):
        return self.disadvtgs

    def get_reviewer(self):
        return self.reviewer

    def get_date(self):
        return self.date