from collections import Counter

from flask import request, render_template

import utils.db_models
from utils import db_models
from utils.common import transformation_raw_to_dict
from utils.db_models import Category, Dishes, OrderedDishes


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
    order_ids = utils.db_models.db_session.query(OrderedDishes.order_id).where(OrderedDishes.dish_id == dish_id).distinct().all()
    order_ids_dict = transformation_raw_to_dict(["order_id"], order_ids)
    order_ids = [n["order_id"] for n in order_ids_dict]
    suggested_dishes = utils.db_models.db_session.query(OrderedDishes.dish_id, OrderedDishes.count).where(
        OrderedDishes.order_id.in_(order_ids)).all()
    suggested_dishes_totals = {}
    for suggested_dish in suggested_dishes:
        suggested_dish_id, quantity = suggested_dish
        if dish_id != suggested_dish_id:
            if suggested_dish_id in suggested_dishes_totals:
                suggested_dishes_totals[suggested_dish_id] += quantity
            else:
                suggested_dishes_totals[suggested_dish_id] = quantity
    suggested_dishes_top = sorted(suggested_dishes_totals, key=suggested_dishes_totals.get, reverse=True)[:3]
    return render_template("menu.html", dishes=[dish], suggested_dishes_top=suggested_dishes_top)


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
