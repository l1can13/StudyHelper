from config import host, user, password, db_name
import pymysql.cursors


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
        self.general_mark = ''
        self.tech_tasks = ''
        self.teamwork = ''
        self.responsibility = ''
        self.tech_help = ''
        self.user = ''

    def add_review(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `Оценки` (`Общая оценка`, `Решение технических задач`, `Командная работа`, `Ответственность`, `Помощь в решении технических задач`, `User_name`) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_user, (self.general_mark, self.tech_tasks, self.teamwork, self.responsibility, self.tech_help, self.user))
                connection.commit()
        finally:
            connection.close()

    def set_username(self, username):
        self.user = username

    def set_general_mark(self, general_mark):
        self.general_mark = general_mark

    def set_tech_tasks(self, tech_tasks):
        self.tech_tasks = tech_tasks

    def set_teamwork(self, teamwork):
        self.teamwork = teamwork

    def set_responsibility(self, responsibility):
        self.responsibility = responsibility

    def set_tech_help(self, tech_help):
        self.tech_help = tech_help

    def get_user(self):
        return self.user

    def get_general_mark(self):
        return self.general_mark

    def get_tech_tasks(self):
        return self.tech_tasks

    def get_teamwork(self):
        return self.teamwork

    def get_responsibility(self):
        return self.responsibility

    def get_tech_help(self):
        return self.tech_help
