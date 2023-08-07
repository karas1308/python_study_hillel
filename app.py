from flask import Flask, request
import sqlite3

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
    if request.method == "GET":
        # /user?phone=3801111111111
        args = request.args
        phone = args.get('phone')
        if phone:
            con = sqlite3.connect("dish.db")
            new_cur = con.cursor()
            res = new_cur.execute(f"SELECT * FROM User where phone='{phone}'")
            results = res.fetchall()
            con.close()
            return results
        else:
            return "specify user's phone"


@app.route("/user/register", methods=["POST"])
def user_register():
    pass


@app.route("/user/sign_in", methods=["POST"])
def user_sign_in():
    pass


@app.route("/user/logout", methods=["POST"])
def user_logout():
    pass


@app.route("/user/restore", methods=["POST"])
def user_restore():
    pass


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


@app.route("/menu", methods=["GET"])
def menu():
    con = sqlite3.connect("dish.db")
    new_cur = con.cursor()
    res = new_cur.execute("SELECT * FROM Dishes")
    results = res.fetchall()
    con.close()
    return results


@app.route("/menu/<cat_name>", methods=["GET"])
def menu_category(cat_name):
    # /menu/first
    con = sqlite3.connect("dish.db")
    new_cur = con.cursor()
    res = new_cur.execute(f"SELECT * FROM Category WHERE name='{cat_name}'")
    results = res.fetchall()
    con.close()
    return results


@app.route("/menu/<cat_name>/<dish>", methods=["GET"])
def menu_dish(cat_name, dish):
    # /menu/first/borshch
    con = sqlite3.connect("dish.db")
    new_cur = con.cursor()
    res = new_cur.execute(f"SELECT * FROM Dishes WHERE category='{cat_name}' AND dish_name='{dish}'")
    results = res.fetchall()
    con.close()
    return results


@app.route("/menu/<cat_name>/<dish>/review", methods=["POST"])
def menu_dish_review(cat_name, dish):
    pass


@app.route("/menu/search", methods=["POST"])
def menu_search():
    pass


@app.route("/admin/menu", methods=["GET", "POST", "PUT", "DELETE"])
def admin_menu():
    pass


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
