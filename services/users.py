from flask import request, session, redirect, render_template

from utils.sql_lite import SQLiteDB


def add_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            db.insert_into("User", data)
        users = db.select_from("User", ["*"])
    return render_template("register_page.html", users=users)


def login_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            if session.get("user_id"):
                # user logged
                return redirect("/")
            data = request.form.to_dict()
            users_data = db.select_from("User", ["id", "phone", "name", "password", "type"],
                                        where={"phone": data["phone"]})
            if users_data and users_data[0]["password"] == data["password"]:
                session["user_id"] = users_data[0]["id"]
                session["user_phone"] = users_data[0]["phone"]
                session["user_type"] = users_data[0]["type"]
                session["user_name"] = users_data[0]["name"]
                return redirect("/")
            else:
                return "якась лажа"
        users = db.select_from("User", ["*"])
    return render_template("login_page.html", users=users)


def log_out_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            session["user_id"] = None
            session["user_phone"] = None
            return redirect("/")
            # return "User logged out. Пока пока"
        users = db.select_from("User", ["*"])
    return render_template("logout_page.html", users=users)


def get_user():
    user = ""
    if request.method == "GET":
        if session.get("user_id"):
            with SQLiteDB("dish.db") as db:
                user = db.select_from("User", ["*"], where={"id": session["user_id"]})
    return render_template("user_info.html", user=user)


def change_user_password():
    data = request.form.to_dict()
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            db.update_column_value("User", {"password": data["new_password"]}, where={"phone": data["phone"]})
        user = db.select_from("User", ["*"])
    return render_template("restore_password.html", user=user)


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
