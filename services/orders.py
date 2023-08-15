from flask import session, request


def start_cart():
    if session.get("user_id"):
        data = request.form.to_dict()
        request.json.get('dish_id')
        # need to added dish_id
        session["dishes_to_order"] = [data]
    return data
