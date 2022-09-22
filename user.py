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
            self.username = args[0]
        elif len(args) == 2:
            self.username = args[0]
            self.teamname = args[1]
        else:
            self.username = None
            self.teamname = None

    def set_team(self, teamname):
        self.teamname = teamname

    def get_team(self):
        return self.teamname

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def add_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `Пользователи` (`Имя`, `Фамилия`, `user_name`, `team`, `role`) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(insert_user) # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()
        finally:
            connection.close()
