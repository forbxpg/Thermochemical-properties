import json
import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()

from helpers.parsers import STATE_MAPPING
from caloric_calc import JanafCalculator, IvtCalculator


PARSED_DATA_PATH = os.getenv("PARSED_DATA")
IVT_PATH = f"{PARSED_DATA_PATH}/ivt.json"
JANAF = f"{PARSED_DATA_PATH}/janaf.json"


def get_data(filename):
    with open(filename, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def find_substance(data, name, state):
    if state in STATE_MAPPING:
        state = STATE_MAPPING[state]
    for substance in data:
        if name == substance.get("name") and state == substance.get("state"):
            return substance
    return None


def calculate(
    substance: dict, t: Union[int, float], calculate_ivt: bool = False
) -> Union[dict, None]:
    calculator = (
        IvtCalculator(substance) if calculate_ivt else JanafCalculator(substance)
    )
    t = t * 10 ** (-4) if calculate_ivt else t
    for temp_range in substance.get("ranges"):
        if temp_range.get("min") <= t <= temp_range.get("max"):
            coefficients = temp_range.get("coefficients")
            return {
                "Entropy": calculator.get_entropy(t, coefficients),
                "Enthalpy": calculator.get_enthalpy(t, coefficients) / 1000,
                "Heat": calculator.get_heat(t, coefficients),
                "MolarMass": substance.get("molar_mass"),
            }
    return None


def main():
    while True:
        try:
            name = input('Введите название вещества или "exit" для выхода: ')
            if name == "exit":
                print("Выход из программы.")
                break
            state = input("Введите состояние (s, l, g): ")
            t = float(input("Введите температуру: "))
            calculate_ivt = (
                input("Посчитать для IVT?(сейчас JANAF) [y/n]: ").lower() == "y"
            )
            calculate_ivt = True if calculate_ivt == "y" else False
            data = get_data(IVT_PATH if calculate_ivt else JANAF)
            substance = find_substance(data, name, state)
            if substance:
                result = calculate(substance, t, calculate_ivt)
                if result:
                    print(
                        f"Результаты для {name} ({state}) при {t}K:\n"
                        f"Энтропия: {result['Entropy']}\n"
                        f"Энтальпия: {result['Enthalpy']}\n"
                        f"Теплоемкость: {result['Heat']}\n"
                        f"Молярная масса: {result['MolarMass']}"
                    )
                else:
                    print(f"Нет данных для {name} в заданном диапазоне температур.")
            else:
                print(f"{name} не найдено в базе данных.")
        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректные данные.")


if __name__ == "__main__":
    main()
