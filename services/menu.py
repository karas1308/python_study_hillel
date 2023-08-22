from flask import request, render_template

from utils import database, db_models
from utils.db_models import Category, Dishes
from utils.sql_lite import SQLiteDB


def menu_actions():
    database.init_db()
    dishes = database.db_session.query(db_models.Dishes).all()
    return render_template("menu.html", dishes=dishes)


def get_category(cat_name):
    database.init_db()
    categories = database.db_session.query(Category).where(Category.name == cat_name).all()
    return render_template("categories.html", categories=categories)


def get_dish(cat_name, dish_id):
    database.init_db()
    dish = database.db_session.query(Dishes).where((Dishes.category == cat_name) & (Dishes.id == dish_id)).one()
    return render_template("menu.html", dishes=[dish])


def search_dish():
    database.init_db()
    data = request.form.to_dict()
    if request.method == "POST":
        dishes = database.db_session.query(Dishes).filter(Dishes.dish_name.like(f'%{data["search"]}%')).all()
        return render_template("menu.html", dishes=dishes)
    else:
        "Nothing found"


def welcome_page():
    database.init_db()
    dishes = database.db_session.query(Dishes).all()
    return render_template("menu.html", dishes=dishes)
