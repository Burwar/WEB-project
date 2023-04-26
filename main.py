import sqlite3
import os
from flask import Flask, render_template, url_for, request, redirect, make_response, g, flash, abort
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


DATABASE = '/base/base.db'
DEBUG = True
SECRET_KEY = 'zwegcgyhuirsj52486swrdtf '
MAX_CONTENT_LEN = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, "base.db")))

login_manager = LoginManager(app)


def connect_db():
    connect = sqlite3.connect(app.config["DATABASE"])
    connect.row_factory = sqlite3.Row
    return connect


def create_db():
    db = connect_db()
    with app.open_resource("db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
@app.route("/main")
def main():
    db = get_db()
    dbase = DataBase(db)
    return render_template("main.html", title="Главная страница", menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route("/add_post", methods=["GET", "POST"])
@login_required
def addPost():
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        if len(request.form["name"]) > 4 and len(request.form["post"]) > 10:
            res = dbase.addPost(request.form["name"], request.form["url"], request.form["type"], request.form["post"])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return render_template("add_post.html", title="Добавление статьи", menu=dbase.getMenu())


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = DataBase(db)
    name, post = dbase.getPost(alias)
    if not name:
        abort(404)
    return render_template("post.html", title=name, post=post, menu=dbase.getMenu())



@app.route("/autorisation", methods=["GET", "POST"])
def autorisation():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        user = dbase.getUserByLogin(request.form["login"])
        if user and check_password_hash(user["password"], request.form["password"]):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get("remainme") else False
            login_user(userlogin, remember=rm)
            return redirect(url_for("main"))
        print("Неверная пара логин/пароль")
    return render_template("autorisation.html", title="Авторизация", menu=dbase.getMenu())


@app.route("/registrate", methods=["GET", "POST"])
def registrate():
    db = get_db()
    dbase = DataBase(db)
    a = True
    if request.method == "POST":
        if a:
            hash = generate_password_hash(request.form["password"])
            res = dbase.addUser(request.form["name1"], request.form["name2"], request.form["name3"],
                                request.form["sex"], request.form["tel"], request.form["email"],
                                request.form["login"], hash)
            if res:
                return redirect(url_for("autorisation"))
            else:
                print("Ошибка добавления статьи в БД")
        else:
            print("Неверно заполнены поля")
    return render_template("registrate.html", title="Регистрация", menu=dbase.getMenu())


@app.route("/profile")
@login_required
def profile():
    db = get_db()
    dbase = DataBase(db)
    return render_template("profile.html", title="Профиль", menu=dbase.getMenu())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("autorisation"))


@app.route("/userava")
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    a = make_response(img)
    a.headers["Content-Type"] = "image/png"
    return a


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    print("Ошибка обновления аватара")
            except FileExistsError as err:
                print("Ошибка чтения файла")
        else:
            print("Ошибка обновления аватара")
    return redirect(url_for("profile"))


@app.errorhandler(404)
def pageNotFound(error):
    db = get_db()
    dbase = DataBase(db)
    return render_template("page404.html", title="Страница не найдена", menu=dbase.getMenu())


@app.errorhandler(401)
def notEnoughUserAccess(error):
    db = get_db()
    dbase = DataBase(db)
    return render_template("page401.html", title="Страница не доступна", menu=dbase.getMenu())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    dbase = DataBase(db)
    return UserLogin().fromDB(user_id, dbase)


if __name__ == '__main__':
    app.run(debug=True)