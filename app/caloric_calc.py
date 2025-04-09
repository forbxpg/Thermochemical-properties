from abc import ABC, abstractmethod
from math import log
from typing import Union


class Calculator(ABC):
    """Abstract class gives interface for calculators."""

    def __init__(self, substance: dict) -> None:
        self.substance = substance

    @abstractmethod
    def get_entropy(self, t: int, coefficients: dict) -> float:
        pass

    @abstractmethod
    def get_enthalpy(self, t: int, coefficients: dict) -> float:
        pass

    @abstractmethod
    def get_heat(self, t: int, coefficients: dict) -> float:
        pass


class JanafCalculator(Calculator):
    """
    Calculator for Janaf database.

    Realize entropy, enthalpy and heat calculations.
    """

    def get_entropy(self, t: int, coefficients: dict) -> float:
        """Return entropy value for given temperature and coefficients."""
        a, b, c, d, e, f, g, h = coefficients.values()
        return round(
            8.314
            * (
                a * log(t)
                + b * t
                + (c / 2) * (t**2)
                + (d / 3) * (t**3)
                + (e / 4) * (t**4)
                + g
                - (h / 2) * (t ** (-2))
            ),
            2,
        )

    def get_enthalpy(self, t: int, coefficients: dict) -> float:
        """Return enthalpy value for given temperature and coefficients."""
        a, b, c, d, e, f, g, h = coefficients.values()
        return round(
            (
                8.314
                * t
                * (
                    a
                    + (b / 2) * t
                    + (c / 3) * (t**2)
                    + (d / 4) * (t**3)
                    + (e / 5) * (t**4)
                    + f * (t ** (-1))
                    - h * (t ** (-2))
                )
            ),
            2,
        )

    def get_heat(self, t: int, coefficients: dict) -> float:
        """Return heat value for given temperature and coefficients."""
        a, b, c, d, e, f, g, h = coefficients.values()
        return round(
            (
                8.314
                * (a + b * t + c * (t**2) + d * (t**3) + e * (t**4) + h * (t ** (-2)))
            ),
            2,
        )


class IvtCalculator(Calculator):
    """
    Calculator for Ivtanthermo database.

    Realize entropy, enthalpy and heat calculations.
    """

    def get_entropy(self, t: int, coefficients: dict) -> float:
        """Return entropy value for given temperature and coefficients."""
        a, b, c, d, e, f, g = coefficients.values()
        return round(
            a
            + b * log(t)
            + b
            - c * t ** (-2)
            + 2 * e * t
            + 3 * f * (t**2)
            + 4 * g * (t**3),
            2,
        )

    def get_enthalpy(self, t: int, coefficients: dict) -> float:
        """Return enthalpy value for given temperature and coefficients."""
        a, b, c, d, e, f, g = coefficients.values()
        return round(
            (
                b * t
                - 2 * c * (t ** (-1))
                - d
                + e * (t**2)
                + 2 * f * (t**3)
                + 3 * g * (t**4)
            )
            * 10
            - self.substance.get("enthalpy_diff"),
            2,
        )

    def get_heat(self, t: int, coefficients: dict) -> float:
        """Return heat value for given temperature and coefficients."""
        a, b, c, d, e, f, g = coefficients.values()
        return round(
            (b + 2 * c * (t ** (-2)) + 2 * e * t + 6 * f * (t**2) + 12 * g * (t**3)),
            2,
        )


class BkwCalculator(JanafCalculator):
    """Calculates BKW-data for JANAF database."""

    def get_x(self, t: int, properties: dict) -> float:
        alpha, beta, kappa, theta = properties.values()
        return alpha
