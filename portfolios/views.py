from django.shortcuts import render, redirect
from .forms import ProfileForm, PublicationForm, TeachingForm

SECTIONS = [
    'Personal Info', 'Professional Bio', 'Research Interests',
    'Publications', 'Teaching Load', 'Contact Details',
]

def showInfo(request):
    return render(request, 'portfolios/showInfo.html')

def dark_template1_preview(request):
    return render(request, 'portfolios/dark_template1.html')

def dark_template2_preview(request):
    return render(request, 'portfolios/dark_template2.html')

def light_template1_preview(request):
    return render(request, 'portfolios/light_template1.html')

def light_template2_preview(request):
    return render(request, 'portfolios/light_template2.html')

def step_one(request):
    return render(request, 'portfolios/step_one.html')

def step_two(request):
    profile_form = ProfileForm()
    context = {
        'profile_form': profile_form,
        'sections': SECTIONS,
    }
    return render(request, 'portfolios/step_two.html', context)

def step_three(request):
    return render(request, 'portfolios/step_three.html')
