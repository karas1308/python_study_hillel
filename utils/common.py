from flask import session


def transformation_raw_to_dict(keys: list, raw_data: list):
    result = []
    # transformation RAW to dict
    for n in raw_data:
        result_dict = dict.fromkeys(keys)
        for key, value in zip(result_dict.keys(), n):
            result_dict[key] = value
        result.append(result_dict)
    return result


def check_is_admin(function):
    def wrapper():
        if session.get("user_type") == 2:
            func = function()
            return func
        else:
            return "Only admin has access"

    return wrapper
