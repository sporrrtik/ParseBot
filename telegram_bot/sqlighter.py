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
            result = self.cursor.execute("SELECT * FROM `Logins` WHERE `Login` = ?", (login,)).fetchone()
            return bool(len(result))

    def data_is_correct(self, login, password):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Logins` WHERE `Login` = ? AND `Password` = ?", (login, password)).fetchall()
            return bool(len(result))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

