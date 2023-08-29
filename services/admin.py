from sqlite3 import IntegrityError

from flask import session, request, render_template, redirect

import utils.db_models
from utils.common import check_is_admin
from utils.db_models import Category, Dishes


@check_is_admin
def admin_category_actions():
    if session.get("user_id"):
        utils.db_models.init_db()
        if request.method == "POST":
            data = request.form.to_dict()
            try:
                category = Category(
                    cat_id=data["category_name"].replace(" ", "_").lower(),
                    name=data["category_name"]
                )
                utils.db_models.db_session.add(category)
                utils.db_models.db_session.commit()
            except IntegrityError:
                return "Category should be unique"
        # if request.method == "PUT":
        #     data = request.form.to_dict()
        #     db.update_column_value("Category",
        #                            {"id": data["new_category_name"], "name": data["new_category_name"]},
        #                            where={"id": data["old_category_name"]})
        data = utils.db_models.db_session.query(Category)
        return render_template("create_category.html", categories=data)
    else:
        return redirect("/user/sign_in")


@check_is_admin
def admin_menu_actions():
    if session.get("user_id"):
        utils.db_models.init_db()
        if request.method == "POST":
            data = request.form.to_dict()
            dish = Dishes(
                dish_id=data.get("dish_name").replace(" ", "_"),
                dish_name=data.get("dish_name"),
                price=data.get("price"),
                description=data.get("description"),
                available=1,
                photo=data.get("photo"),
                ccal=data.get("ccal"),
                protein=data.get("protein"),
                fat=data.get("fat"),
                carb=data.get("carb"),
                category=data.get("category")

            )
            utils.db_models.db_session.add(dish)
            utils.db_models.db_session.commit()
        dishes = utils.db_models.db_session.query(Dishes).all()
        return render_template("add_dish.html", dishes=dishes)
    else:
        return redirect("/user/sign_in")
