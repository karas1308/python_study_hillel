from flask import request, session, redirect, render_template

import utils.db_models
from utils.db_models import User, Orders
from utils.sql_lite import SQLiteDB


def add_user():
    utils.db_models.init_db()
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
            utils.db_models.db_session.add(user)
            utils.db_models.db_session.commit()
        users = utils.db_models.db_session.query(User).all()
    return render_template("register_page.html", users=users)


def login_user():
    utils.db_models.init_db()
    if request.method == "POST":
        if session.get("user_id"):
            # user logged
            return redirect("/")
        data = request.form.to_dict()
        fields = ["id", "phone", "name", "password", "type"]
        users_data = (utils.db_models.db_session.query(User.id, User.phone, User.name, User.password, User.type)
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
    users = utils.db_models.db_session.query(User).all()
    return render_template("login_page.html", users=users)


def log_out_user():
    if request.method == "POST":
        session["user_id"] = None
        session["user_phone"] = None
        return redirect("/")
        # return "User logged out. Пока пока"
    utils.db_models.init_db()
    users = utils.db_models.db_session.query(User).all()
    return render_template("logout_page.html", users=users)


def get_user():
    if session.get("user_id"):
        utils.db_models.init_db()
        user = utils.db_models.db_session.query(User).where(User.id == session["user_id"]).one()
        return render_template("user_info.html", user=user)
    else:
        return redirect("/")


def change_user_password():
    data = request.form.to_dict()
    if request.method == "POST":
        utils.db_models.init_db()
        if data.get("password"):
            utils.db_models.db_session.query(User).update({User.password == data.get("password")})
        else:
            return "Password can not be empty"
    users = utils.db_models.db_session.query(User).all()
    return render_template("restore_password.html", user=users)


def get_user_orders():
    if session.get("user_id"):
        utils.db_models.init_db()
        orders = utils.db_models.db_session.query(Orders).where(Orders.user == session["user_id"]).all()
        if orders:
            return render_template("user_orders.html", orders=orders)
        else:
            return "No orders"
    return redirect("/user/sign_in")


def get_user_order_by_id(order_id):
    # can be used order id only coz it is unique
    utils.db_models.init_db()
    if session.get("user_id"):
        order = utils.db_models.db_session.query(Orders).where(
            (Orders.user == session["user_id"]) & (Orders.id == order_id)).one()
        return render_template("user_order.html", order=order)
    else:
        return redirect("/user/sign_in")
