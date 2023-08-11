from flask import request

from utils.sql_lite import SQLiteDB


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
