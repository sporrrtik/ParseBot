import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `Users` WHERE `id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_to_news(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `News` (`id`) VALUES (?)", (user_id,))

    def add_subscriber(self, user_id, date, status=True):
        """Добавляем нового подписчика"""
        self.add_to_news(user_id)
        with self.connection:
            return self.cursor.execute("INSERT INTO `Users` (`id`, `Subscribtion`, `Date`) VALUES(?,?, ?)",
                                       (user_id, status, date))

    def update_subscription(self, user_id, date, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET `Subscribtion` = ?, `Date` = ? WHERE `id` = ?",
                                       (status, date, user_id))

    def update_news_subscription(self, user_id, news, status):
        """Изменяем статус подписки на новостные рассылки"""
        with self.connection:
            return self.cursor.execute("UPDATE `News` SET `" + news + "` = ? WHERE `id` = ?", (status, user_id))

    def user_subscribed(self, user_id):
        """Проверяем подписку пользователя"""
        with self.connection:
            result = self.cursor.execute("SELECT `Subscribtion` FROM `Users` WHERE `id` = ?", (user_id,)).fetchone()
            print(result)
            return result

    def check_news_subscription(self, user_id, news):
        """Проверяем, подписан ли пользователь на новость"""
        with self.connection:
            return self.cursor.execute("SELECT `" + news + "` FROM `News` WHERE id = ?", (user_id,)).fetchone()

    def get_all_subscribers(self, news):
        """Достаём список всех подписчиков на новость"""
        with self.connection:
            # return self.cursor.execute("SELECT `" + news + "` FROM `News` WHERE  = 1")
            return self.cursor.execute("SELECT `id` FROM `News` WHERE `" + news + "` = 1")

    def add_user(self, login, password):
        """Вносим логин и пароль пользователя в базу данных"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `Logins` (`Login`, `Password`) VALUES (?, ?)",
                                       (login, password))

    def login_is_used(self, login):
        """Достаём список всех логинов"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Logins` WHERE `Login` = ?", (login,)).fetchall()
            return bool(len(result))

    def data_is_correct(self, login, password):
        """Проверяем правильность логина и пароля"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Logins` WHERE `Login` = ? AND `Password` = ?",
                                         (login, password)).fetchall()
            return bool(len(result))

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute('SELECT `id` FROM `Users` WHERE `Subscribtion` = 1').fetchall()

    def ban_user(self, user_id, date):
        """Баним пользователя"""
        with self.connection:
            return self.cursor.execute('INSERT INTO `Banned` (`id`,`Date`, `Time`) VALUES(?, ?, ?)',
                                       (user_id, date, 5))

    def user_is_banned(self, user_id, date):
        """Проверяем забанен ли пользователь"""
        with self.connection:
            ban_date = self.cursor.execute('SELECT `Date` FROM `Banned` WHERE `id` = ?',(user_id,)).fetchall()
            if ban_date and (int(ban_date[0][0][11:13]) == int(str(date)[11:13])):
                time = self.cursor.execute('SELECT `Time` FROM `Banned` WHERE `id` = ?',(user_id,)).fetchall()
                return (time[0][0] + int(ban_date[0][0][14:16])) % 60 >= int(str(date)[14:16])
            return False

    def login_as_admin(self, login):
        """Проверяем является ли юзер админом"""
        with self.connection:
            return self.cursor.execute("SELECT `Admin` FROM `Logins` WHERE `Login` = ?",(login,)).fetchall()

    def delete_from_database(self, table, column, data):
        """Удаляем что угодно откуда угодно"""
        with self.connection:
            return self.cursor.execute("DELETE FROM `" + table + "` WHERE `" + column + "` = ?",(data,))

    def insert_tel_id(self, id, login):
        """Добавляем tel_id в таблицу к пользователю"""
        with self.connection:
            return self.cursor.execute("UPDATE `Logins` SET `tel_id` = ? WHERE `Login` = ?",(id ,login))

    def get_tel_id(self, login):
        """Достаём tel_id по логину"""
        with self.connection:
            return self.cursor.execute("SELECT `tel_id` FROM `Logins` WHERE `Login` = ?", (login,)).fetchone()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
