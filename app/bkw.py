from pprint import pprint
from helpers.parsers import parse_janaf


BKW_PATH = "/Users/forbxpg/PycharmProjects/thermodynamics/initial_data/bkw.txt"
JANAF = "/Users/forbxpg/PycharmProjects/thermodynamics/initial_data/janaf.txt"


def get_bkw_data(bkw_path: str = BKW_PATH):
    with open(bkw_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        d = {}
        for line in lines[1:]:
            name, kappa_i = line.strip().split()
            d[name] = float(kappa_i)
        return d


pprint(get_bkw_data())


# def fill_janaf_data_with_bkw():
#     janaf_data = parse_janaf(JANAF)
#     bkw_data = get_bkw_data()
#     res = []
#     for substance in janaf_data:
#         for
#         if substance["name"] in bkw_data["substances"] and substance["state"] == "gas":
#             res.append(substance)
#     return res


# print(fill_janaf_data_with_bkw())
