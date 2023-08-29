from flask import request, session, redirect, render_template

import utils.db_models
from utils.common import transformation_raw_to_dict
from utils.db_models import User, Orders, OrderedDishes, Dishes


def add_user():
    utils.db_models.init_db()
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
        user = utils.db_models.db_session.query(User).where(User.id == session["user_id"]).one_or_none()
        if user:
            return render_template("user_info.html", user=user)
        else:
            return redirect("/")
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
        ordered_dishes = utils.db_models.db_session.query(Orders.id,
                                                          Orders.order_date,
                                                          Dishes.dish_name,
                                                          Dishes.category,
                                                          Dishes.price,
                                                          OrderedDishes.count,
                                                          Dishes.ccal,
                                                          Dishes.fat,
                                                          Dishes.carb,
                                                          Dishes.protein,
                                                          Dishes.description,
                                                          ).join(OrderedDishes, Orders.id == OrderedDishes.order_id
                                                                 ).join(Dishes, Dishes.id == OrderedDishes.dish_id
                                                                        ).where(Orders.user == session["user_id"]).all()
        if ordered_dishes:
            fields = ["id", "order_date", "dish_name", "category", "price", "count", "ccal", "fat", "carb", "protein",
                      "description"]
            __ordered_dishes = transformation_raw_to_dict(fields, ordered_dishes)
            orders = []
            for ordered_dish in __ordered_dishes:
                if not any(("id", ordered_dish["id"]) in order.items() for order in orders):
                    orders.append({"id": ordered_dish["id"], "dishes": [], "total": 0, "total_ccal": 0})
                if any(("id", ordered_dish["id"]) in order.items() for order in orders):
                    for order in orders:
                        if order["id"] == ordered_dish["id"]:
                            order["dishes"].append(ordered_dish)
                            order["total"] += ordered_dish["count"] * ordered_dish["price"]
                            order["total_ccal"] += ordered_dish["count"] * ordered_dish["ccal"]
                            order["order_date"] = ordered_dish["order_date"].strftime("%Y-%m-%dT%H:%M:%SZ")

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
