from flask import request

from utils.sql_lite import SQLiteDB

test_user_id = 1


def add_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            db.insert_into("User", data)
        users = db.select_from("User", ["*"])
    html_form = f"""
       <form method="POST">
           <input type="text" name="email" placeholder="email">
           <input type="text" name="last_name" placeholder="last_name">
           <input type="text" name="name" placeholder="name">
           <input type="text" name="password" placeholder="password">
           <input type="text" name="phone" placeholder="phone">
           <input type="text" name="tg" placeholder="tg">
           <input type="type" name="type" placeholder="type">
           <input type="submit">
       </form>
       {str(users)}
       """
    return html_form


def login_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            users_data = db.select_from("User", ["phone", "password"], where={"phone": data["phone"]})
            if users_data and users_data[0]["password"] == data["password"]:
                return "User logged in"
            else:
                return "якась лажа"
        users = db.select_from("User", ["*"])
    html_form = f"""
       <form method="POST">
           <input type="text" name="password" placeholder="password">
           <input type="text" name="phone" placeholder="phone">
           <input type="submit">
       </form>
       {str(users)}
       """
    return html_form


def log_out_user():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            return "User logged out. Пока пока"
        users = db.select_from("User", ["*"])
    html_form = f"""
       <form method="POST">
           <input type="submit">
       </form>
       {str(users)}
       """
    return html_form


def get_user():
    if request.method == "GET":
        # /user?phone=3801111111111
        args = request.args
        phone = args.get('phone')
        if phone:
            with SQLiteDB("dish.db") as db:
                user = db.select_from("User", ["*"], where={"phone": phone})
            return user
        else:
            return "specify user's phone"


def change_user_password():
    data = request.form.to_dict()
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            db.update_column_value("User", "password", data["new_password"], where={"phone": data["phone"]})
        user = db.select_from("User", ["*"])
    html_form = f"""
       <form method="POST">
           <input type="text" name="phone" placeholder="phone">
           <input type="text" name="new_password" placeholder="new_password">
           <input type="submit">
       </form>
       {str(user)}
    """
    return html_form


def get_user_orders():
    with SQLiteDB("dish.db") as db:
        orders = db.select_from("Orders", ["*"], where={"user": test_user_id})
    return orders


def get_user_order_by_id(order_id):
    # can be used order id only coz it is unique
    with SQLiteDB("dish.db") as db:
        orders = db.select_from("Orders", ["*"], where=f"user={test_user_id} and id={order_id}")
    return orders
