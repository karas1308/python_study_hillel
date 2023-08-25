from flask import request, render_template

import utils.db_models
from utils import db_models
from utils.db_models import Category, Dishes


def menu_actions():
    utils.db_models.init_db()
    dishes = utils.db_models.db_session.query(db_models.Dishes).all()
    return render_template("menu.html", dishes=dishes)


def get_category(cat_name):
    utils.db_models.init_db()
    categories = utils.db_models.db_session.query(Category).where(Category.name == cat_name).all()
    return render_template("categories.html", categories=categories)


def get_dish(cat_name, dish_id):
    utils.db_models.init_db()
    dish = utils.db_models.db_session.query(Dishes).where((Dishes.category == cat_name) & (Dishes.id == dish_id)).one()
    return render_template("menu.html", dishes=[dish])


def search_dish():
    utils.db_models.init_db()
    data = request.form.to_dict()
    if request.method == "POST":
        dishes = utils.db_models.db_session.query(Dishes).filter(Dishes.dish_name.like(f'%{data["search"]}%')).all()
        return render_template("menu.html", dishes=dishes)
    else:
        "Nothing found"


def welcome_page():
    utils.db_models.init_db()
    dishes = utils.db_models.db_session.query(Dishes).all()
    return render_template("menu.html", dishes=dishes)
