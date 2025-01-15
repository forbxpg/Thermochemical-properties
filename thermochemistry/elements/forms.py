from django import forms

from .models import Element


class TemperatureForm(forms.Form):
    temperature = forms.FloatField(required=True)


class ElementForm(forms.ModelForm):

    class Meta:
        model = Element
        fields = (
            'name',
            'state',
        )
