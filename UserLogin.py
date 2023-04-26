from flask import url_for


class UserLogin():
    def fromDB(self, user_id, db):
        self.user = db.getUser(user_id)
        return self

    def create(self, user):
        self.user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user["id"])

    def getName1(self):
        return self.user['name1'] if self.user else "Без имени"

    def getName2(self):
        return self.user['name2'] if self.user else "Без фамилии"

    def getName3(self):
        return self.user['name3'] if self.user else "Без отчества"

    def getSex(self):
        return self.user['sex'] if self.user else "Без пола"

    def getTel(self):
        return self.user['tel'] if self.user else "Без номера телефона"

    def getEmail(self):
        return self.user['email'] if self.user else "Без почты"

    def getAvatar(self, app):
        img = None
        if not self.user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for("static", filename="image/default.png"), "rb") as f:
                    img = f.read()
            except FileExistsError as err:
                print("Не найден аватар по умолчанию: " + str(err))
        else:
            img = self.user['avatar']
        return img

    def verifyExt(self, filename):
        ext = filename.rsplit(".", 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False