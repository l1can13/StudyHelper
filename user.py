from config import host, user, password, db_name
import pymysql.cursors


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


class User:
    def __init__(self, *args):
        if len(args) == 1:
            self.name = args[0]
            self.counter_of_people = 0
        elif len(args) == 2:
            self.name = args[0]
            self.surname = args[1]
            self.counter_of_people = 0
        elif len(args) == 3:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.counter_of_people = 0
        elif len(args) == 4:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.counter_of_people = 0
        elif len(args) == 5:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.counter_of_people = 0
        elif len(args) == 6:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.role = args[5]
            self.counter_of_people = 0
        elif len(args) == 7:
            self.name = args[0]
            self.surname = args[1]
            self.group = args[2]
            self.username = args[3]
            self.teamname = args[4]
            self.role = args[5]
            self.tg_id = args[6]
            self.counter_of_people = 0
            self.invite_code = None
            self.db_id = None
            self.team_id = None
        else:
            self.name = None
            self.surname = None
            self.group = None
            self.username = None
            self.teamname = None
            self.role = None
            self.tg_id = 0
            self.counter_of_people = 0

    def set_db_id(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `user_id` FROM `users` WHERE `tg_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.tg_id)
                result = cursor.fetchone()
                connection.commit()
                if result:
                    self.db_id = result['user_id']
                else:
                    self.db_id = -1
        finally:
            connection.close()

    # функция для получения фамилий из бд для определенной группы
    def get_team_members(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # sql_request = "SELECT `Имя` FROM `Пользователи` WHERE `Команда` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `name` FROM `users` WHERE `user_id` IN (SELECT `user_id` FROM `team_members` WHERE `team_id` IN (SELECT `team_id` FROM `teams` WHERE `team_name` = %s)) and `user_id` != %s and `user_id` not in (select `assessored_user_id` from `team_members_ratings` where `assessor_user_id` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.teamname, self.db_id, self.db_id))
                result = cursor.fetchall()
                connection.commit()
                return result
        finally:
            connection.close()

    def get_db_id_from_db(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `user_id` FROM `users` WHERE `tg_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.tg_id)
                result = cursor.fetchone()
                connection.commit()
                return result['user_id']
        finally:
            connection.close()

    def set_invite_code(self, invite_code):
        self.invite_code = invite_code

    def get_invite_code(self):
        return self.invite_code

    def get_counter_of_people(self):
        return self.counter_of_people

    def set_counter_of_people(self, counter):
        self.counter_of_people = counter

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_surname(self, surname):
        self.surname = surname

    def get_surname(self):
        return self.surname

    def set_group(self, group):
        self.group = group

    def get_group(self):
        return self.group

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_team_id(self):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `team_id` FROM `teams` WHERE `team_name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.teamname)
                result = cursor.fetchone()
                connection.commit()
                self.team_id = result['team_id']
        finally:
            connection.close()

    def get_team_id(self):
        return self.team_id

    def set_teamname(self, teamname):
        self.teamname = teamname

    def get_teamname(self):
        return self.teamname

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def set_tg_id(self, arg):
        self.tg_id = arg

    def get_tg_id(self):
        return self.tg_id

    def get_db_id(self):
        return self.db_id

    def add_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # insert_user = "INSERT INTO `Пользователи` (`Имя`, `Группа`, `User_name`, `Команда`, `Роль`, `Ид`) VALUES (%s, %s, %s, %s, %s, %s);"
                insert_user = "INSERT INTO `users` (`tg_id`) VALUES (%s);"
                cursor.execute(insert_user,
                               self.tg_id)  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()

                self.set_db_id()
        finally:
            connection.close()

    def add_user_to_team_members(self):
        self.set_team_id()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `team_members` (`team_id`, `user_id`, `role`, `invite_code`) VALUES (%s, %s, %s, %s);"
                cursor.execute(insert_user, (self.team_id, self.db_id, self.role,
                                             self.invite_code))  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()
        finally:
            connection.close()

    def update_user_id_in_team_members(self):
        self.set_db_id()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "UPDATE `team_members` SET `user_id` = %s WHERE `invite_code` = %s"
                cursor.execute(insert_user, (self.db_id, self.invite_code))
                connection.commit()
        finally:
            connection.close()

    def delete_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # delete_user = "DELETE FROM `Пользователи` WHERE `Ид` = %s"
                delete_user = "DELETE FROM `users` WHERE `user_id` = %s"
                cursor.execute(delete_user, self.db_id)
                connection.commit()

                delete_user = "DELETE FROM `team_members` WHERE `user_id` = %s"
                cursor.execute(delete_user, self.db_id)
                connection.commit()
        finally:
            connection.close()

    def add_name(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "UPDATE `Пользователи` SET `Имя` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                sql_request = "UPDATE `users` SET `name` = %s WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.name, self.db_id))
                connection.commit()
        finally:
            connection.close()

    def add_username(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "UPDATE `Пользователи` SET `User_name` = %s WHERE `Ид` = %s"  # строка для SQL-запроса
                sql_request = "UPDATE `users` SET `tg_username` = %s WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.username, self.db_id))
                connection.commit()
        finally:
            connection.close()

    def add_group(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "UPDATE `users` SET `group_num` = %s WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.group, self.db_id))
                connection.commit()
        finally:
            connection.close()

    def get_role_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT `Роль` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `role` FROM `team_members` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                role = cursor.fetchone()
                connection.commit()
                return role['role']
        finally:
            connection.close()

    def get_teamname_from_bd(self):
        self.set_db_id()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT `Команда` FROM `Пользователи` WHERE `Ид` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `team_name` FROM `teams` WHERE `team_id` = (SELECT `team_id` FROM `team_members` WHERE `user_id` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                tmnm = cursor.fetchone()
                connection.commit()
                return tmnm['team_name']
        finally:
            connection.close()

    # Метод для проверки наличия пользователя в команде
    def is_in_team(self):
        self.set_db_id()
        connection = connect_to_db()
        check = ''
        try:
            with connection.cursor() as cursor:
                # user_from_db = "SELECT `Команда` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"
                user_from_db = "SELECT `team_id` FROM `team_members` WHERE `user_id` = %s"
                cursor.execute(user_from_db, self.db_id)
                check = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True

    def is_admin(self):
        connection = connect_to_db()
        check = ''
        try:
            with connection.cursor() as cursor:
                # user_from_db = "SELECT `Название` FROM `Команды` WHERE `Ид` = %s"
                user_from_db = "SELECT `team_name` FROM `teams` WHERE `admin_user_id` = %s"
                cursor.execute(user_from_db, self.db_id)
                check = cursor.fetchall()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True

    def check_team_with_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `team_id` FROM `team_members` WHERE `invite_code` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                if result:
                    return True
                return False
        finally:
            connection.close()

    def get_team_using_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # sql_request = "SELECT `Команда` FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `team_name` FROM `teams` WHERE `team_id` IN (SELECT `team_id` FROM `team_members` WHERE `invite_code` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                for row in result:
                    return row['team_name']
        finally:
            connection.close()

    def get_role_using_code(self, code):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # sql_request = "SELECT `Роль` FROM `Коды` WHERE `Код` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `role` FROM `team_members` WHERE `invite_code` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, code)
                result = cursor.fetchall()
                connection.commit()
                for row in result:
                    return row['role']
        finally:
            connection.close()

    def update_id_in_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "UPDATE `Пользователи` SET `Ид` = %s WHERE `Команда` = %s AND `Роль` = %s"  # строка для SQL-запроса
                sql_request = "UPDATE `users` SET `tg_id` = %s WHERE `user_id` IN (SELECT `user_id` FROM `team_members` WHERE `team_id` IN (SELECT `team_id` FROM `teams` WHERE `team_name` = %s) AND `role` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.tg_id, self.teamname, self.role))
                connection.commit()
        finally:
            connection.close()

    def get_name_from_bd(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # sql_request = "SELECT `Имя` FROM `Пользователи` WHERE `Ид` = %s or `User_name` = %s"  # строка для SQL-запроса
                sql_request = "SELECT `name` FROM `users` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                role = cursor.fetchone()
                connection.commit()
                return role['name']
        finally:
            connection.close()

    # def add_report(self):
    #     connection = connect_to_db()
    #     try:
    #         with connection.cursor() as cursor:
    #             sql_request = "INSERT INTO `Отчеты` (`Имя пользователя`, `Автор отчета`, `Текст отчета`, `Дата отправки`) VALUES (%s, %s, %s, %s);"  # строка для SQL-запроса
    #             cursor.execute(sql_request, (self.username, self.id, self.report, self.departure_time))
    #             connection.commit()
    #     finally:
    #         connection.close()
