from flask import Flask, request, url_for


from services.admin import admin_category_actions, admin_menu_actions
from services.menu import search_dish, menu_actions, get_category, get_dish, welcome_page
from services.orders import get_cart, update_cart_data, delete_cart_item, add_cart_item, make_order
from services.users import add_user, login_user, log_out_user, get_user, change_user_password, get_user_orders, \
    get_user_order_by_id

app = Flask(__name__)
app.secret_key = "qwerty123456"


@app.route("/", methods=["GET", "POST"])
def hello():
    return welcome_page()


@app.route("/cart", methods=["GET", "POST"])
def cart():
    return get_cart()


@app.route("/cart/update", methods=["POST"])
def cart_update():
    update_cart_data()
    app.redirect(url_for('cart'))
    return get_cart()


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    delete_cart_item()
    app.redirect(url_for('cart'))
    return get_cart()


@app.route("/cart/order", methods=["POST"])
def cart_order():
    make_order()
    return welcome_page()


@app.route("/cart/add", methods=["POST"])
def cart_add():
    add_cart_item()
    return get_cart()


@app.route("/user", methods=["GET"])
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
    return get_user_orders()


@app.route("/user/orders/<order_id>", methods=["GET"])
def user_order(order_id):
    return get_user_order_by_id(order_id)


@app.route("/user/address", methods=["GET", "POST"])
def user_addresses():
    pass


@app.route("/user/address/<address_id>", methods=["GET", "PUT", "DELETE"])
def user_address(address_id):
    pass


@app.route("/menu", methods=["GET", "POST"])
def menu():
    return menu_actions()


@app.route("/menu/<cat_name>", methods=["GET"])
def menu_category(cat_name):
    # /menu/first
    return get_category(cat_name)


@app.route("/menu/<cat_name>/<dish_id>", methods=["GET"])
def menu_dish(cat_name, dish_id):
    # /menu/first/borshch
    return get_dish(cat_name, dish_id)


@app.route("/menu/<cat_name>/<dish>/review", methods=["POST"])
def menu_dish_review(cat_name, dish):
    pass


@app.route("/menu/search/", methods=["GET", "POST"])
def menu_search():
    return search_dish()


@app.route("/admin/menu/category", methods=["GET", "POST"])
def admin_menu_category():
    return admin_category_actions()


@app.route("/admin/menu", methods=["GET", "POST"])
def admin_menu():
    return admin_menu_actions()


@app.route("/admin/menu/<cat_name>", methods=["GET", "POST"])
def admin_menu_category_name(cat_name):
    if request.method == "GET":
        # /admin/menu/first
        return menu_category(cat_name)


@app.route("/admin/menu/<cat_name>/<dish>", methods=["GET", "POST"])
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
    app.run(host="0.0.0.0")
