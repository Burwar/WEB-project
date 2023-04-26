import sqlite3
from flask import url_for
import re


class DataBase:
    def __init__(self, db):
        self.db = db
        self.cur = db.cursor()

    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, name, url, t, text):
        try:
            self.cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.cur.fetchone()
            if res["count"] > 0:
                print("Статья с таким url уже существует")
                return False
            self.cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (name, url, t, text))
            self.db.commit()
        except sqlite3.Error as err:
            print("Ошибка добавления статьи в БД " + str(err))
            return False
        return True

    def getPost(self, alias):
        try:
            self.cur.execute(f"SELECT name, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.cur.fetchone()
            if res:
                return res
        except sqlite3.Error as err:
            print("Ошибка получения статьи в БД " + str(err))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.cur.execute(f"SELECT id, name, url, text From posts")
            res = self.cur.fetchall()
            if res:
                return res
        except sqlite3.Error as err:
            print("Ошибка получения статьи в БД " + str(err))
        return []

    def addUser(self, name1, name2, name3, sex, tel, email, login, password):
        try:
            self.cur.execute(f"SELECT COUNT() as `count` FROM users WHERE tel LIKE '{tel}'")
            res = self.cur.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким телефоном уже существует")
                return False
            self.cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.cur.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким email уже существует")
                return False
            self.cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, NULL)",
                             (name1, name2, name3, sex, tel, email, login, password))
            self.db.commit()
        except sqlite3.Error as err:
            print("Ошибка добавления пользователя в БД " + str(err))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as err:
            print("Ошибка получения данных в БД " + str(err))
        return False

    def getUserByLogin(self, login):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE login = {login} LIMIT 1")
            res = self.cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as err:
            print("Ошибка получения данных в БД " + str(err))
        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.db.commit()
        except sqlite3.Error as err:
            print("Ошибка обновления аватара в БД " + str(err))
            return False
        return True