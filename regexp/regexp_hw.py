import re


def find_all(regexp, text):
    s = [n.lstrip() for n in re.findall(regexp, text)]
    print(s)


def matcher(regexp, data: list):
    res_correct = []
    res_wrong = []
    for n in data:
        if re.match(regexp, str(n)):
            res_correct.append(n)
        else:
            res_wrong.append(n)
    print(f"Match: {res_correct}")
    print(f"Do not match: {res_wrong}")


list_time = ["7:23", "12:38", "12:61", "12:60", "4:35", "9:59", "00:00", "6:20", "9:09", "12:12", "25:08", "36:05"]
list_time_str = "7:23, 12:38, 12:61, 12:60, 4:35, 9:59, 00:00, 6:20, 9:09, 12:12, 25:08, 36:05"
list_numbers = [1984, 245, 1845, 2019, 2000, 1987, 2250, 2301, 2402]
list_numbers_str = "1984, 245, 1845 2019, 2000, 1987, 2250, 2301, 2402"

matcher("([0-1]?[0-9]|2[0-3]):[0-5][0-9]", list_time)
find_all(r'\b([0-1][0-9]:[0-5][0-9]|[0-9]:[0-5][0-9]|[2][0-3]:[0-5][0-9])\b', list_time_str)
matcher("^(19\d{2}|2[0-2]\d{2}|2300)$", list_numbers)
find_all("(19\d{2}|2[0-2]\d{2}|2300)", list_numbers_str)
