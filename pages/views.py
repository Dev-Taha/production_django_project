
from django.views import generic
from django.shortcuts import render, redirect 


class Landing (generic.TemplateView):
    template_name = 'pages/landing.html'

