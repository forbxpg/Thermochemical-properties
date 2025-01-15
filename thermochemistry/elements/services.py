from math import log

import numpy as np


def calculate(coefficients, temperature):
    temp = temperature * 10 ** (-4)
    a = coefficients.a
    b = coefficients.b
    c = coefficients.c
    d = coefficients.d
    e = coefficients.e
    f = coefficients.f
    g = coefficients.g

    heat = b + 2 * c * \
        temp ** (-2) + 2 * e * temp + 6 * f * \
        temp ** 2 + 12 * g * temp ** 3
    entropy = a + b * log(temp) + b - c * temp ** (-2) + \
        2 * e * temp + 3 * f * temp ** 2 + 4 * g * temp ** 3
    enthalpy = (b * temp - 2 * c * temp ** (-1) - d + e * temp ** 2 + 2 *
                f * temp ** 3 + 3 * g * temp ** 4) * 10

    context = {
        'heat': heat,
        'entropy': entropy,
        'enthalpy': enthalpy,
    }
    return context


def generate_property_table(element):
    Tmin = min([r.Tmin for r in element.ranges.all()])
    Tmax = max([r.Tmax for r in element.ranges.all()])
    step = 100

    temperatures = np.arange(Tmin, Tmax + step, step)
    property_values = []
    for t in temperatures:
        for range_data in element.ranges.all():
            if range_data.Tmin <= t <= range_data.Tmax:
                coefficients = range_data.coefficients
                heat = round(calculate(coefficients, t)['heat'], 3)
                entropy = round(calculate(coefficients, t)['entropy'], 3)
                enthalpy = round(calculate(coefficients, t)['enthalpy'] - element.enthalpy_diff, 3)
                property_values.append((t, heat, entropy, enthalpy))
                break
    return property_values
