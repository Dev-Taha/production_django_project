from urllib import request

from django.shortcuts import render
from django.views import generic


class Landing (generic.TemplateView):
    template_name = 'pages/landing.html'

