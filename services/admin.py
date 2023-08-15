from sqlite3 import IntegrityError

from flask import session, request, render_template, redirect

from utils.sql_lite import SQLiteDB


def admin_menu_actions():
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


def adm_menu():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            data["id"] = data["dish_name"].replace(" ", "_")
            data["available"] = 1
            db.insert_into("Dishes", data)
        dishes = db.select_from("Dishes", ["*"])
    return render_template("add_dish.html", dishes=dishes)
