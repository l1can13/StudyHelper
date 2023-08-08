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
            self.tg_id = None
            self.db_id = None
            self.team_id = None
            self.counter_of_people = 0

    def set_db_id_from_db(self):
        self.db_id = self.get_db_id_from_db()

    def get_team_id_from_db(self):
        self.set_db_id_from_db()
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "SELECT `team_id` FROM `team_members` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                result = cursor.fetchone()
                connection.commit()

                return result['team_id'] if result else -1
        finally:
            connection.close()

    # функция для получения фамилий из бд для определенной группы
    def get_teammates_only_names(self):
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

                return result['user_id'] if result else -1
        finally:
            connection.close()

    def set_db_id(self, db_id):
        self.db_id = db_id

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

    def set_team_id_by_db(self):
        self.team_id = self.get_team_id_from_db()

    def set_team_id(self, team_id):
        self.team_id = team_id

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

    @staticmethod
    def add_empty_user():
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `users` (`name`, `group_num`, `tg_id`) VALUES (%s, %s, %s);"
                cursor.execute(insert_user,
                               ('invited_user',
                                'INVT',
                                None))  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()

                return cursor.lastrowid
        finally:
            connection.close()

    def add(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # insert_user = "INSERT INTO `Пользователи` (`Имя`, `Группа`, `User_name`, `Команда`, `Роль`, `Ид`) VALUES (%s, %s, %s, %s, %s, %s);"
                insert_user = "INSERT INTO `users` (`name`, `group_num`, `tg_id`) VALUES (%s, %s, %s);"
                cursor.execute(insert_user,
                               (self.name, self.group,
                                self.tg_id))  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()

                self.set_db_id_from_db()

                insert_user = "INSERT INTO `all_bot_identifiers` VALUES (%s) ON DUPLICATE KEY UPDATE telegram_id=VALUES(telegram_id);"
                cursor.execute(insert_user, self.tg_id)
                connection.commit()
        finally:
            connection.close()

    def add_user(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                # insert_user = "INSERT INTO `Пользователи` (`Имя`, `Группа`, `User_name`, `Команда`, `Роль`, `Ид`) VALUES (%s, %s, %s, %s, %s, %s);"
                insert_user = "INSERT INTO `users` (`tg_id`) VALUES (%s);"
                cursor.execute(insert_user,
                               self.tg_id)  # cursor.execute(insert_user, (Сюда переменные через запятую, которые надо добавть в таблицу.))
                connection.commit()

                self.set_db_id_from_db()
        finally:
            connection.close()

    def add_user_to_team_members(self):
        if self.team_id is None:
            self.set_team_id_by_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "INSERT INTO `team_members` (`team_id`, `user_id`, `role`) VALUES (%s, %s, %s);"
                cursor.execute(insert_user, (self.team_id, self.db_id, self.role))
                connection.commit()
        finally:
            connection.close()

    @staticmethod
    def delete_user_from_users_by_id(user_id):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                insert_user = "DELETE FROM `users`" \
                              "WHERE `user_id` = %s"
                cursor.execute(insert_user, user_id)
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
        self.set_db_id_from_db()
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

    def get_product_from_db(self):
        self.set_db_id_from_db()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `product_name` FROM `teams` WHERE `team_id` = (SELECT `team_id` FROM `team_members` WHERE `user_id` = %s)"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                product_name = cursor.fetchone()
                connection.commit()
                return product_name['product_name']
        finally:
            connection.close()

    def get_teammates(self):
        if self.team_id is None:
            self.set_team_id_by_db()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `users`.`name`, `team_members`.`role` " \
                              "FROM `users` " \
                              "INNER JOIN `team_members` ON `users`.`user_id` = `team_members`.`user_id` " \
                              "WHERE `team_members`.`team_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.team_id)
                teammates = cursor.fetchall()
                connection.commit()

            return teammates
        finally:
            connection.close()

    def get_team_code(self):
        if self.team_id is None:
            self.set_team_id_by_db()
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = ("SELECT `code` from `teams` "
                               "WHERE team_id = %s")
                cursor.execute(sql_request, self.team_id)
                code = cursor.fetchone()
                connection.commit()

            return code['code'] if code is not None else None
        finally:
            connection.close()

    def get_teammates_excludes_me(self):
        if self.team_id is None:
            self.set_team_id_by_db()
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `users`.`name`, `team_members`.`role` " \
                              "FROM `users` " \
                              "INNER JOIN `team_members` ON `users`.`user_id` = `team_members`.`user_id` " \
                              "WHERE `team_members`.`team_id` = %s and `team_members`.`user_id` != %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.team_id, self.db_id))
                teammates = cursor.fetchall()
                connection.commit()

            return teammates
        finally:
            connection.close()

    def get_reports(self):
        if self.db_id is None:
            self.set_db_id_from_db()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `sprint_num`, `report_text`, `report_date`" \
                              "FROM `sprint_reports`" \
                              "WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                teammates = cursor.fetchall()
                connection.commit()

            return teammates
        finally:
            connection.close()

    # Метод для проверки наличия пользователя в команде
    def is_in_team(self):
        if self.db_id is None:
            self.set_db_id_from_db()
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
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
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
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

    def is_exists(self):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                user_from_db = "SELECT `user_id` FROM `users` WHERE `tg_id` = %s"
                cursor.execute(user_from_db, self.tg_id)
                check = cursor.fetchone()
                connection.commit()
        finally:
            connection.close()
        if not check:
            return False
        return True

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

    def update_invited_user(self, user_id):
        connection = connect_to_db()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql_request = "UPDATE `users`" \
                              "SET `name` = %s," \
                              "`group_num` = %s," \
                              "`tg_id` = %s " \
                              "WHERE `user_id` = %s"
                cursor.execute(sql_request, (self.name, self.group, self.tg_id, user_id))
                connection.commit()

                insert_user = "INSERT INTO `all_bot_identifiers` VALUES (%s) ON DUPLICATE KEY UPDATE telegram_id=VALUES(telegram_id);"
                cursor.execute(insert_user, self.tg_id)
                connection.commit()
        finally:
            connection.close()

    def get_who_evaluated_me(self):
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `users`.`name` " \
                              "FROM `users`" \
                              "INNER JOIN `team_members_ratings` ON `team_members_ratings`.`assessor_user_id` = `users`.`user_id`" \
                              "WHERE `team_members_ratings`.`assessored_user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                user_result = cursor.fetchall()
                connection.commit()

                return user_result
        finally:
            connection.close()

    def get_count_teammates(self):
        if self.team_id is None:
            self.set_team_id_by_db()
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT COUNT(`users`.`user_id`) as count_teammates " \
                              "FROM `users` " \
                              "INNER JOIN `team_members` ON `users`.`user_id` = `team_members`.`user_id` " \
                              "WHERE `team_members`.`team_id` = %s and `team_members`.`user_id` != %s"  # строка для SQL-запроса
                cursor.execute(sql_request, (self.team_id, self.db_id))
                count_teammates = cursor.fetchone()
                connection.commit()

            return count_teammates
        finally:
            connection.close()

    @staticmethod
    def get_name_by_id(user_id):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `name` FROM `users` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, user_id)
                user_result = cursor.fetchone()
                connection.commit()
                return user_result['name']
        finally:
            connection.close()

    @staticmethod
    def get_id_by_name(name):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `user_id` FROM `users` WHERE `name` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, name)
                user_result = cursor.fetchone()
                connection.commit()
                return user_result['user_id']
        finally:
            connection.close()

    @staticmethod
    def get_tg_id_by_user_id(user_id):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `tg_id` FROM `users` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, user_id)
                user_result = cursor.fetchone()
                connection.commit()
                return user_result['tg_id']
        finally:
            connection.close()

    @staticmethod
    def delete_user_from_team(user_id):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "DELETE FROM `team_members` WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, user_id)
                connection.commit()
        finally:
            connection.close()

    @staticmethod
    def get_all_tg_ids():
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `telegram_id` FROM `all_bot_identifiers`"  # строка для SQL-запроса
                cursor.execute(sql_request)
                ids = cursor.fetchall()
                connection.commit()
                return ids
        finally:
            connection.close()

    def get_name_from_db(self):
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `name` FROM `users`" \
                              "WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                user_result = cursor.fetchone()
                connection.commit()
                return user_result['name']
        finally:
            connection.close()

    def get_group_from_db(self):
        if self.db_id is None:
            self.set_db_id_from_db()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql_request = "SELECT `group_num` FROM `users`" \
                              "WHERE `user_id` = %s"  # строка для SQL-запроса
                cursor.execute(sql_request, self.db_id)
                group_num = cursor.fetchone()
                connection.commit()
                return group_num['group_num']
        finally:
            connection.close()

    @staticmethod
    def get_user_from_db(tg_id):
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                sql_request = ("SELECT `users`.`user_id`, `users`.`name`, `users`.`group_num`, `team_members`.team_id, `team_members`.role, `teams`.team_name "
                               "FROM `users` "
                               "LEFT JOIN `team_members` ON `users`.user_id = `team_members`.user_id "
                               "LEFT JOIN `teams` ON `team_members`.team_id = `teams`.team_id "
                               "WHERE `users`.`tg_id` = %s")
                cursor.execute(sql_request, tg_id)

                user_from_users = cursor.fetchone()
                connection.commit()

                if user_from_users is None:
                    user_result = User()
                    user_result.set_tg_id(tg_id)

                    return user_result

                user_result = User()

                user_result.set_tg_id(tg_id)
                user_result.set_db_id(user_from_users['user_id'])
                user_result.set_name(user_from_users['name'])
                user_result.set_group(user_from_users['group_num'])
                user_result.set_team_id(user_from_users['team_id'])
                user_result.set_role(user_from_users['role'])
                user_result.set_teamname(user_from_users['team_name'])

                return user_result
        finally:
            connection.close()
