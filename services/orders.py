from datetime import datetime

import flask
from flask import session, render_template, request

from logger import log
from utils.sql_lite import SQLiteDB

dishes_in_cart = []


def get_cart():
    if session.get("user_id"):
        with SQLiteDB("dish.db") as db:
            cart = db.select_from("Orders", ["id"],
                                  where=f"user={session.get('user_id')} AND status=0", fetch_all=False)
            if cart:
                session["cart_id"] = cart["id"]
                field_to_select = ("dish_name, category, ccal, fat, carb, description, count, price, photo, "
                                   "Ordered_dishes.id as id")
                dishes = db.select_from(row_query=f"SELECT {field_to_select} from Ordered_dishes JOIN Dishes on "
                                                  f"Dishes.id = Ordered_dishes.dish_id WHERE "
                                                  f"Ordered_dishes.order_id = {cart['id']}")
                session["dishes_in_cart"] = dishes
                for dish in dishes:
                    dish["total"] = dish["count"] * dish["price"]
                    dish["fat"] = dish["count"] * dish["fat"]
                    dish["carb"] = dish["count"] * dish["carb"]
                    dish["ccal"] = dish["count"] * dish["ccal"]

                return render_template("cart.html", dishes=dishes)
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
                    "count": data["count"],
                    "order_id": cart["id"],
                    "dish_id": data["dish_id"]
                }
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
