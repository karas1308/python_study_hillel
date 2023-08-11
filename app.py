from flask import Flask, request, jsonify
import sqlite3

from services.menu import search_dish
from services.users import add_user, login_user, log_out_user, get_user, change_user_password
from utils.sql_lite import SQLiteDB

app = Flask(__name__)


@app.route("/")
def welcome_page():
    return "Welcome"


@app.route("/cart", methods=["GET", "PUT"])
def cart():
    pass


@app.route("/cart/order", methods=["POST"])
def cart_order():
    pass


@app.route("/cart/add", methods=["POST"])
def cart_add():
    pass


@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    return get_user()


@app.route("/user/register", methods=["GET", "POST"])
# GET added to avoid error on direct call from browser
def user_register():
    return add_user()


@app.route("/user/sign_in", methods=["GET", "POST"])
def user_sign_in():
    return login_user()


@app.route("/user/logout", methods=["GET", "POST"])
def user_logout():
    return log_out_user()


@app.route("/user/restore", methods=["GET", "POST"])
def user_restore():
    return change_user_password()


@app.route("/user/orders", methods=["GET"])
def user_orders_history():
    pass


@app.route("/user/orders/<order_id>", methods=["GET"])
def user_order(order_id):
    pass


@app.route("/user/address", methods=["GET", "POST"])
def user_addresses():
    pass


@app.route("/user/address/<address_id>", methods=["GET", "PUT", "DELETE"])
def user_address(address_id):
    pass


@app.route("/menu", methods=["GET", "POST"])
def menu():
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


@app.route("/menu/<cat_name>", methods=["GET"])
def menu_category(cat_name):
    # /menu/first
    with SQLiteDB("dish.db") as db:
        results = db.select_from("Category", ["*"], where={"name": cat_name})
    return results


@app.route("/menu/<cat_name>/<dish>", methods=["GET"])
def menu_dish(cat_name, dish):
    # /menu/first/borshch
    with SQLiteDB("dish.db") as db:
        results = db.select_from("Dishes", ["*"], where=f"category='{cat_name}' AND dish_name='{dish}'")
    return results


@app.route("/menu/<cat_name>/<dish>/review", methods=["POST"])
def menu_dish_review(cat_name, dish):
    pass


@app.route("/menu/search/", methods=["GET", "POST"])
def menu_search():
    return search_dish()


@app.route("/admin/menu", methods=["GET", "POST", "PUT", "DELETE"])
def admin_menu():
    with SQLiteDB("dish.db") as db:
        data = db.insert_into("Category", {"id": "second", "name": "second"})
    return str(data)


@app.route("/admin/menu/<cat_name>", methods=["GET", "POST", "PUT", "DELETE"])
def admin_menu_category(cat_name):
    if request.method == "GET":
        # /admin/menu/first
        return menu_category(cat_name)


@app.route("/admin/menu/<cat_name>/<dish>", methods=["GET", "POST", "PUT", "DELETE"])
def admin_menu_dish(cat_name, dish):
    pass


@app.route("/admin/orders", methods=["POST"])
def admin_orders():
    args = request.args
    show_active_only = args.get('active')
    if show_active_only:
        pass


@app.route("/admin/orders/<order_id>", methods=["GET", "PUT"])
def admin_order_id(order_id):
    pass


@app.route("/admin/search", methods=["POST"])
def admin_search():
    menu_search()


if __name__ == "__main__":
    app.run()
