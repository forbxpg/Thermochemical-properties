"""Views for pages."""
from django.views.generic import TemplateView
from django.shortcuts import render

from elements.models import Element
from .forms import SearchForm


class HomeTemplateView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            elements = Element.objects.filter(name__icontains=name)[:7]
            context = {
                'form': form,
                'elements': elements,
            }
        return render(request, self.template_name, context)

class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'
