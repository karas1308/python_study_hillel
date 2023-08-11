from flask import request

from utils.sql_lite import SQLiteDB


def menu_actions():
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            data = request.form.to_dict()
            data["id"] = data["dish_name"].replace(" ", "_")
            data["available"] = 1
            db.insert_into("Dishes", data)
        dishes = db.select_from("Dishes", ["*"])
    html_form = f"""
    <form method="POST">
        <input type="text" name="dish_name" placeholder="name">
        <input type="text" name="price" placeholder="price">
        <input type="text" name="description" placeholder="description">
        <input type="text" name="photo" placeholder="photo">
        <input type="text" name="ccal" placeholder="ccal">
        <input type="text" name="protein" placeholder="protein">
        <input type="text" name="fat" placeholder="fat">
        <input type="text" name="carb" placeholder="carb">
        <input type="text" name="category" placeholder="category">
        <input type="submit">
    </form>
    <br>
    {str(dishes)}
    """
    return html_form


def get_category(cat_name):
    with SQLiteDB("dish.db") as db:
        results = db.select_from("Category", ["*"], where={"name": cat_name})
    return results


def get_dish(cat_name, dish_name):
    with SQLiteDB("dish.db") as db:
        results = db.select_from("Dishes", ["*"], where=f"category='{cat_name}' AND dish_name='{dish_name}'")
    return results

def search_dish():
    data = request.form.to_dict()
    results = ""
    with SQLiteDB("dish.db") as db:
        if request.method == "POST":
            results = db.select_from("Dishes", ["*"], where={"dish_name": data["dish_name"]})
        if not results:
            results = db.select_from("Dishes", ["*"])
            results = f"ALL RESULTS: {results}"
    html_form = f"""
           <form method="POST">
               <input type="text" name="dish_name" placeholder="dish_name">
               <input type="submit">
           </form>
           {str(results)}
        """
    return html_form
