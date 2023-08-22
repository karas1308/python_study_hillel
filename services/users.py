from flask import request, session, redirect, render_template

from utils import database
from utils.db_models import User
from utils.sql_lite import SQLiteDB


def add_user():
    database.init_db()
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            user = User(
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
                password=data.get("password"),
                tg=data.get("tg"),
                last_name=data.get("last_name"),
            )
            database.db_session.add(user)
            database.db_session.commit()
        users = database.db_session.query(User).all()
    return render_template("register_page.html", users=users)


def login_user():
    database.init_db()
    if request.method == "POST":
        if session.get("user_id"):
            # user logged
            return redirect("/")
        data = request.form.to_dict()
        fields = ["id", "phone", "name", "password", "type"]
        users_data = (database.db_session.query(User.id, User.phone, User.name, User.password, User.type)
                      .where(User.phone == data["phone"]).one())
        result_dict = dict.fromkeys(fields)
        for key, value in zip(result_dict.keys(), users_data):
            result_dict[key] = value
        if result_dict and result_dict["password"] == data["password"]:
            session["user_id"] = result_dict["id"]
            session["user_phone"] = result_dict["phone"]
            session["user_type"] = result_dict["type"]
            session["user_name"] = result_dict["name"]
            return redirect("/")
        else:
            return "якась лажа"
    users = database.db_session.query(User).all()
    return render_template("login_page.html", users=users)


def log_out_user():
    if request.method == "POST":
        session["user_id"] = None
        session["user_phone"] = None
        return redirect("/")
        # return "User logged out. Пока пока"
    database.init_db()
    users = database.db_session.query(User).all()
    return render_template("logout_page.html", users=users)


def get_user():
    if session.get("user_id"):
        database.init_db()
        user = database.db_session.query(User).where(User.id == session["user_id"]).one()
        return render_template("user_info.html", user=user)
    else:
        return redirect("/")


def change_user_password():
    data = request.form.to_dict()
    if request.method == "POST":
        database.init_db()
        if data.get("password"):
            database.db_session.query(User).update(User.password == data.get("password"))
        else:
            return "Password can not be empty"
    users = database.db_session.query(User).all()
    return render_template("restore_password.html", user=users)


def get_user_orders():
    with SQLiteDB("dish.db") as db:
        if session.get("user_id"):
            orders = db.select_from("Orders", ["*"], where={"user": session["user_id"]})
            return render_template("user_orders.html", orders=orders)
        else:
            return redirect("/user/sign_in")


def get_user_order_by_id(order_id):
    # can be used order id only coz it is unique
    with SQLiteDB("dish.db") as db:
        if session.get("user_id"):
            order = db.select_from("Orders", ["*"], where=f"user={session['user_id']} and id={order_id}")
            return render_template("user_order.html", orders=order)
        else:
            return redirect("/user/sign_in")
