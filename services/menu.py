from flask import request, render_template

from utils import database, db_models
from utils.db_models import Category, Dishes
from utils.sql_lite import SQLiteDB


def menu_actions():
    database.init_db()
    dishes = database.db_session.query(db_models.Dishes).all()
    # with SQLiteDB("dish.db") as db:
    #     if request.method == "POST":
    #         data = request.form.to_dict()
    #         data["id"] = data["dish_id"].replace(" ", "_")
    #         data["available"] = 1
    #         db.insert_into("Dishes", data)
    #     dishes = db.select_from("Dishes", ["*"])
    return render_template("menu.html", dishes=dishes)


def get_category(cat_name):
    database.init_db()
    categories = database.db_session.query(Category).where(Category.name == cat_name).all()
    # with SQLiteDB("dish.db") as db:
    #     categories = db.select_from("Category", ["*"], where={"name": cat_name})
    return render_template("categories.html", categories=categories)


def get_dish(cat_name, dish_id):
    database.init_db()
    dish = database.db_session.query(Dishes).where((Dishes.category == cat_name) & (Dishes.id == dish_id)).one()
    # with SQLiteDB("dish.db") as db:
    #     dish = db.select_from("Dishes", ["*"], where=f"category='{cat_name}' AND id='{dish_id}'")
    return render_template("menu.html", dishes=[dish])


def search_dish():
    database.init_db()
    with SQLiteDB("dish.db") as db:
        data = request.form.to_dict()
        if request.method == "POST":
            dishes = database.db_session.query(Dishes).filter(Dishes.dish_name.like(f'%{data["search"]}%')).all()
    return render_template("menu.html", dishes=dishes)


def welcome_page():
    database.init_db()
    dishes = database.db_session.query(Dishes).all()
    return render_template("menu.html", dishes=dishes)
