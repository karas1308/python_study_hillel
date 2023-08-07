from flask import Flask

app = Flask(__name__)


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
    pass


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


@app.route("/user/address/<id>", methods=["GET", "PUT", "DELETE"])
def user_address():
    pass


@app.route("/menu", methods=["GET"])
def menu():
    pass


@app.route("/menu/<cat name>", methods=["GET"])
def menu_category():
    pass


@app.route("/menu/<cat name>/<dish>", methods=["GET"])
def menu_dish():
    pass


@app.route("/menu/<cat name>/<dish>/review", methods=["POST"])
def menu_dish_review():
    pass


@app.route("/menu/search", methods=["POST"])
def menu_search():
    pass


if __name__ == "__main__":
    app.run()
