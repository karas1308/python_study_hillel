from datetime import datetime

from flask import session, render_template, request

import utils.db_models
from logger import log
from utils.common import transformation_raw_to_dict
from utils.db_models import Orders, OrderedDishes, Dishes
from utils.sql_lite import SQLiteDB


def get_cart():
    utils.db_models.init_db()
    if session.get("user_id"):
        cart = utils.db_models.db_session.query(Orders).where(
            (Orders.user == session["user_id"]) & (Orders.status == 0)).one_or_none()
        if cart:
            session["cart_id"] = cart.id
            dishes = utils.db_models.db_session.query(OrderedDishes.id,
                                                      Dishes.dish_name,
                                                      Dishes.category,
                                                      Dishes.ccal,
                                                      Dishes.fat,
                                                      Dishes.carb,
                                                      Dishes.description,
                                                      OrderedDishes.count,
                                                      Dishes.price,
                                                      Dishes.photo,
                                                      ).join(Dishes, Dishes.id == OrderedDishes.dish_id).filter(
                OrderedDishes.order_id == cart.id).all()

            fields = ["id", "dish_name", "category", "ccal", "fat", "carb", "description", "count", "price",
                      "photo"]
            ordered_dishes = transformation_raw_to_dict(fields, dishes)
            session["dishes_in_cart"] = ordered_dishes
            for dish in ordered_dishes:
                dish["total"] = dish["count"] * dish["price"]
                dish["fat"] = dish["count"] * dish["fat"]
                dish["carb"] = dish["count"] * dish["carb"]
                dish["ccal"] = dish["count"] * dish["ccal"]

            return render_template("cart.html", dishes=ordered_dishes)
        else:
            return "Cart is empty"


def update_cart_data():
    if session.get("user_id"):
        utils.db_models.init_db()
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                data = request.form.to_dict()
                if data:
                    for dish_id, count in data.items():
                        for dish in session["dishes_in_cart"]:
                            if str(dish_id) == str(dish["id"]) and str(count) != str(dish["count"]):
                                if int(count) == 0:
                                    utils.db_models.db_session.query(OrderedDishes).where(
                                        OrderedDishes.id == int(dish_id)).delete()
                                    utils.db_models.db_session.commit()
                                else:
                                    utils.db_models.db_session.query(OrderedDishes).filter(
                                        OrderedDishes.id == dish_id).update({OrderedDishes.count: count})
                                    utils.db_models.db_session.commit()


def delete_cart_item():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                data = request.form.to_dict()
                if data:
                    for dish_id, count in data.items():
                        if count == "Delete":
                            db.delete_from_table("Ordered_dishes", where={"id": dish_id})


def add_cart_item():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                data = request.form.to_dict()
                cart = db.select_from("Orders", ["id"],
                                      where=f"user={session.get('user_id')} AND status=0", fetch_all=False)
                if not cart:
                    create_new_order()
                    cart = db.select_from("Orders", ["id"],
                                          where=f"user={session.get('user_id')} AND status=0", fetch_all=False)
                session["cart_id"] = cart["id"]
                ordered_dish = {
                    "count": 1,
                    "order_id": cart["id"],
                    "dish_id": ""
                }
                for key, value in data.items():
                    if value == "Add":
                        ordered_dish["dish_id"] = key
                for key, value in data.items():
                    if key.startswith("count_") and key.replace("count_", "") == ordered_dish["dish_id"]:
                        if int(value):
                            ordered_dish["count"] = int(value)
                db.insert_into("Ordered_dishes", ordered_dish)


def create_new_order():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                data = {
                    "user": int(session.get("user_id")),
                    "order_date": str(datetime.utcnow()),
                    "status": 0
                }
                db.insert_into("Orders", data)
                log.info("Order created")


def make_order():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                db.update_column_value("Orders", {"status": 1},
                                       where={"id": session["cart_id"]})
