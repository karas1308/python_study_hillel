from datetime import datetime

from flask import session, render_template, request

from logger import log
from utils import database
from utils.db_models import Orders, OrderedDishes, Dishes
from utils.sql_lite import SQLiteDB

dishes_in_cart = []


def get_cart():
    database.init_db()
    if session.get("user_id"):
        with (SQLiteDB("dish.db") as db):
            # cart = db.select_from("Orders", ["id"],
            #                       where=f"user={session.get('user_id')} AND status=0", fetch_all=False)
            cart = database.db_session.query(Orders).where(
                (Orders.user == session["user_id"]) & (Orders.status == 0)).one_or_none()
            if cart:
                session["cart_id"] = cart.id
                field_to_select = ("dish_name, category, ccal, fat, carb, description, count, price, photo, "
                                   "Ordered_dishes.id as id")
                # dishes = db.select_from(row_query=f"SELECT {field_to_select} from Ordered_dishes JOIN Dishes on "
                #                                   f"Dishes.id = Ordered_dishes.dish_id WHERE "
                #                                   f"Ordered_dishes.order_id = {cart['id']}")

                dishes = database.db_session.query(OrderedDishes.id,
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
                ordered_dishes = []
                # transformation RAW to dict
                for dish in dishes:
                    result_dict = dict.fromkeys(fields)
                    for key, value in zip(result_dict.keys(), dish):
                        result_dict[key] = value
                    ordered_dishes.append(result_dict)
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
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                data = request.form.to_dict()
                if data:
                    for dish_id, count in data.items():
                        for dish in session["dishes_in_cart"]:
                            if str(dish_id) == str(dish["id"]) and str(count) != str(dish["count"]):
                                if int(count) == 0:
                                    db.delete_from_table("Ordered_dishes", where={"id": dish_id})
                                else:
                                    db.update_column_value("Ordered_dishes", {"count": count},
                                                           where={"id": dish_id})


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
                    "order_date": str(datetime.utcnow())
                }
                db.insert_into("Orders", data)
                log.info("Order created")


def make_order():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            if request.method == "POST":
                db.update_column_value("Orders", {"status": 1},
                                       where={"id": session["cart_id"]})
