import json
import os

import logging
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

logger = logging.getLogger("parsers")

JANAF = os.getenv("JANAF_PATH")
IVT = os.getenv("IVT_PATH")
BKW = os.getenv("BKW_PATH")
PARSED_DATA = os.getenv("PARSED_DATA")

STATE_MAPPING = {
    "s": "solid",
    "l": "liquid",
    "g": "gas",
}


def get_data(filename: str, make_ivt: bool = False) -> list[str]:
    encoding = "utf-16" if make_ivt else "utf-8"
    with open(filename, "r", encoding=encoding) as file:
        return file.readlines()


def parse_janaf(
    filename: str,
    make_ivt: bool = False,
) -> list[dict]:
    """Parse txt file and return a list of dicts."""
    lines = get_data(filename, make_ivt=False)
    length = len(lines)
    parsed_data = []
    i = 0
    while i < length:
        line = lines[i].strip()
        if line:
            diapason = int(lines[i + 4].strip())
            substance = {
                "name": str(lines[i].strip().partition("/")[0]),
                "state": str(STATE_MAPPING.get(lines[i + 1].strip())),
                "valence": int(lines[i + 3].split()[0]),
                "molar_mass": float(lines[i + 3].split()[1]),
                "diapason": diapason,
                "ranges": [],
            }
            i += 5
            for _ in range(diapason):
                t_min, t_max = map(float, lines[i].strip().split())

                a, b, c, d = map(float, lines[i + 1].strip().split())
                e, f, g, h = map(float, lines[i + 2].strip().split())
                temp_range = {
                    "min": t_min,
                    "max": t_max,
                    "coefficients": {
                        "a": a,
                        "b": b,
                        "c": c,
                        "d": d,
                        "e": e,
                        "f": f,
                        "g": g,
                        "h": h,
                    },
                }
                substance["ranges"].append(temp_range)
                i += 3
            parsed_data.append(substance)
        else:
            i += 1
    return parsed_data


def parse_ivt(
    filename: str,
) -> list[dict]:
    """Parse ivtanthermo db and return a list of dicts."""
    lines = get_data(filename, make_ivt=True)
    length = len(lines)
    parsed_data = []
    i = 0
    while i < length:
        line = lines[i].strip()
        logger.info("Processing line: %s", line)
        if line:
            molar_mass, enthalpy_298, enthalpy_diff = map(
                float, lines[i + 5].strip().split()
            )
            diapason = int(lines[i + 6].strip())
            substance = {
                "name": str(lines[i].strip().partition("/")[0]),
                "state": STATE_MAPPING.get(lines[i + 3].strip()),
                "molar_mass": molar_mass,
                "enthalpy_298": enthalpy_298,
                "enthalpy_diff": enthalpy_diff,
                "diapason": diapason,
                "ranges": [],
            }
            logger.info("Substance data: %s", substance)
            i += 7
            for _ in range(diapason):
                print(lines[i].strip().split())
                t_min, t_max = map(float, lines[i].strip().split())
                a, b, c = map(float, lines[i + 1].split())
                d, e, f = map(float, lines[i + 2].split())
                temp_range = {
                    "min": t_min,
                    "max": t_max,
                    "coefficients": {
                        "a": a,
                        "b": b,
                        "c": c,
                        "d": d,
                        "e": e,
                        "f": f,
                        "g": float(lines[i + 3]),
                    },
                }
                substance["ranges"].append(temp_range)
                i += 4
            parsed_data.append(substance)
        else:
            i += 1
    return parsed_data


def get_bkw_data(bkw_path: str = BKW):
    with open(bkw_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        d = {}
        for line in lines[1:]:
            name, kappa_i = line.strip().split()
            d[name] = float(kappa_i)
        return d


def fill_janaf_with_bkw():
    bkw_data = get_bkw_data()
    janaf_data = parse_janaf(JANAF)
    print(len(bkw_data))
    res = []
    dic = {}
    for substance in janaf_data:
        if substance["name"] in bkw_data and substance["state"] == "gas":
            substance["kappa_i"] = bkw_data[substance["name"]]
            res.append(substance)
    return res


with open(f"{PARSED_DATA}/bkw_subs.json", "w", encoding="utf-8") as f:
    json.dump(fill_janaf_with_bkw(), f, indent=4)


pprint(fill_janaf_with_bkw())
print(len(fill_janaf_with_bkw()))


# def make_json(
#     output_filename,
#     make_ivt: bool = False,
# ) -> None:
#     """Dump the data into a JSON and save it."""
#     data = parse_ivt(IVT) if make_ivt else parse_janaf(JANAF)
#     with open(output_filename, "w", encoding="utf-8") as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)
#
#
# def main():
#     make_json(f"{PARSED_DATA}/ivt.json", make_ivt=True)
#     make_json(f"{PARSED_DATA}/janaf.json", make_ivt=False)
#
#
# if __name__ == "__main__":
#     main()
