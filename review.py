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
        self.mark = ''
        self.feedback = ''
        self.user = ''

    def add_review(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `Оценки` (`Оценка`, `Комментарий`, `User_name`) VALUES (%s, %s, %s);"
                cursor.execute(insert_user, (self.mark, self.feedback, self.user))
                connection.commit()
        finally:
            connection.close()

    def set_username(self, username):
        self.user = username

    def set_mark(self, mark):
        self.mark = mark

    def set_feedback(self, feedback):
        self.feedback = feedback

    def get_user(self):
        return self.user

    def get_mark(self):
        return self.mark

    def get_feedback(self):
        return self.feedback
