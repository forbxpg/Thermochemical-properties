from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, render
from .models import Element, Ranges
from .forms import ElementForm, TemperatureForm
from .services import generate_property_table, calculate
import json

class ElementsListView(ListView):
    model = Element
    template_name = 'elements/list.html'

    def get_queryset(self):
        return Element.objects.all().filter(id__lte=10)

class ElementsDetailView(DetailView):
    model = Element
    template_name = 'elements/detail.html'
    form_class = ElementForm

    def get_object(self, queryset=None):
        element = get_object_or_404(
            Element.objects.all(),
            pk=self.kwargs['pk']
        )
        return element

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['data'] = self.object.molar_mass
        context['form'] = TemperatureForm()
        context['table'] = None
        context['temperatures'] = json.dumps([])
        context['cp_values'] = json.dumps([])
        context['h_values'] = json.dumps([])
        context['s_values'] = json.dumps([])
        return context

    def post(self, request, *args, **kwargs):
        form = TemperatureForm(request.POST)
        table = None
        if form.is_valid():
            temperature = form.cleaned_data['temperature']
            element = get_object_or_404(
                Element,
                pk=self.kwargs['pk']
            )
            table = generate_property_table(element)
            temperatures = json.dumps([float(row[0]) for row in table])
            cp_values = json.dumps([float(row[1]) for row in table])
            h_values = json.dumps([float(row[2]) for row in table])
            s_values = json.dumps([float(row[3]) for row in table])
        else:
            temperatures = json.dumps([])
            cp_values = json.dumps([])
            h_values = json.dumps([])
            s_values = json.dumps([])

        context = {
            'element': element,
            'form': form,
            'table': table,
            'temperatures': temperatures,
            'cp_values': cp_values,
            'h_values': h_values,
            's_values': s_values,
        }
        return render(request, self.template_name, context)
