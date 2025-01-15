from django.db import models
import re


def format_state(element_name, state):
    state_map = {
        's': 'Solid',
        'l': 'Liquid',
        'g': 'Gas',
    }
    state_code = re.search(r'/([a-zA-Z]+)/', element_name)
    if state_code:
        state = state_map.get(state_code.group(1), state)
        element_name = re.sub(r'/[a-zA-Z]+/', '', element_name)
    return f"{element_name.strip('/')} {state}"


class Coefficients(models.Model):
    """Coefficients model."""

    a = models.FloatField()
    b = models.FloatField()
    c = models.FloatField()
    d = models.FloatField()
    e = models.FloatField()
    f = models.FloatField()
    g = models.FloatField()
    h = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Коэффициент'
        verbose_name_plural = 'Коэффициенты'


class Ranges(models.Model):
    """Ranges model."""

    Tmin = models.FloatField()
    Tmax = models.FloatField()
    coefficients = models.OneToOneField(
        Coefficients,
        on_delete=models.CASCADE,
        verbose_name='Коэффициенты',
        null=True,
        blank=True
    )
    element = models.ForeignKey(
        'Element',
        related_name='ranges',
        on_delete=models.CASCADE,
        verbose_name='Диапазон для элемента',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Диапазон'
        verbose_name_plural = 'Диапазоны'


class Element(models.Model):
    """Element model."""

    name = models.CharField(max_length=15)
    state = models.CharField(max_length=2)
    molar_mass = models.FloatField()
    enthalpy = models.FloatField()
    enthalpy_diff = models.FloatField()
    num_ranges = models.IntegerField()

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    def __str__(self):
        return format_state(self.name, self.state)
