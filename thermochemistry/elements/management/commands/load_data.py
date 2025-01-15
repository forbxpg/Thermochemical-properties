from django.core.management.base import BaseCommand
from elements.models import Element, Ranges, Coefficients
import json


class Command(BaseCommand):
    help = 'Load data from JSON file'

    def handle(self, *args, **kwargs):
        with open('elements/fixtures/data.json', 'r') as file:
            data = json.load(file)

        for element_data in data:
            element = Element(
                name=element_data['name'],
                state=element_data['state'],
                molar_mass=element_data['molar_mass'],
                enthalpy=element_data['enthalpy'],
                enthalpy_diff=element_data['enthalpy_diff'],
                num_ranges=element_data['num_ranges']
            )
            element.save()

            for range_data in element_data['ranges']:
                coefficients_data = range_data['coefficients']
                coefficients = Coefficients.objects.create(
                    a=coefficients_data['a'],
                    b=coefficients_data['b'],
                    c=coefficients_data['c'],
                    d=coefficients_data['d'],
                    e=coefficients_data['e'],
                    f=coefficients_data['f'],
                    g=coefficients_data['g']
                )
                range_instance = Ranges.objects.create(
                    Tmin=range_data['Tmin'],
                    Tmax=range_data['Tmax'],
                    coefficients=coefficients
                )
                element.ranges.add(range_instance)

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))
