from flask import request, render_template

from utils.sql_lite import SQLiteDB


def menu_actions():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            data["id"] = data["dish_name"].replace(" ", "_")
            data["available"] = 1
            db.insert_into("Dishes", data)
        dishes = db.select_from("Dishes", ["*"])
    return render_template("menu.html", dishes=dishes)


def get_category(cat_name):
    with SQLiteDB("dish.db") as db:
        categories = db.select_from("Category", ["*"], where={"name": cat_name})
    return render_template("categories.html", categories=categories)


def get_dish(cat_name, dish_id):
    with SQLiteDB("dish.db") as db:
        dish = db.select_from("Dishes", ["*"], where=f"category='{cat_name}' AND id='{dish_id}'")
    return render_template("menu.html", dishes=dish)


def search_dish():
    data = request.form.to_dict()
    dishes = ""
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            dishes = db.select_from("Dishes", ["*"], where={"id": data["dish_id"]})
    return render_template("menu.html", dishes=dishes)


def welcome_page():
    with SQLiteDB("dish.db") as db:
        dishes = db.select_from("Dishes", ["*"])
    return render_template("menu.html", dishes=dishes)
