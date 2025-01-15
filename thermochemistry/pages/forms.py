from django import forms


class SearchForm(forms.Form):
    name = forms.CharField(label='Name of the substance', max_length=10, required=True)