def transformation_raw_to_dict(keys: list, raw_data: list):
    result = []
    # transformation RAW to dict
    for n in raw_data:
        result_dict = dict.fromkeys(keys)
        for key, value in zip(result_dict.keys(), n):
            result_dict[key] = value
        result.append(result_dict)
    return result
