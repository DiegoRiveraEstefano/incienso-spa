from django.shortcuts import redirect
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'views/index.html'


class About(TemplateView):
    template_name = 'views/about.html'
