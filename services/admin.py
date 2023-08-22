from sqlite3 import IntegrityError

from flask import session, request, render_template, redirect

from utils import database, db_models
from utils.sql_lite import SQLiteDB


def admin_category_actions():
    if session.get("user_id"):
        if session.get("user_type") == 2:
            with SQLiteDB("dish.db") as db:
                if request.method == "POST":
                    data = request.form.to_dict()
                    try:
                        db.insert_into("Category", {"id": data["category_name"], "name": data["category_name"]})
                    except IntegrityError:
                        return "Category should be unique"
                if request.method == "PUT":
                    data = request.form.to_dict()
                    db.update_column_value("Category",
                                           {"id": data["new_category_name"], "name": data["new_category_name"]},
                                           where={"id": data["old_category_name"]})
                data = db.select_from("Category", ["*"])
                return render_template("create_category.html", categories=data)
        else:
            return "Only admin has access"
    else:
        return redirect("/user/sign_in")


def admin_menu_actions():
    database.init_db()
    if request.method == "POST":
        data = request.form.to_dict()
        dish = db_models.Dishes(
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
        database.db_session.add(dish)
        database.db_session.commit()
    dishes = database.db_session.query(db_models.Dishes).all()
    return render_template("add_dish.html", dishes=dishes)
