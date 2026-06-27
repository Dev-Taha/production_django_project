
from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import User


def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    user = User.objects.get(id=request.session['user_id'])
    
    return render(request, 'dashboard/dashboard.html', {'user': user})

def templates_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'dashboard/templates_dashboard.html', {'user': user})

def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'dashboard/setting_dashboard.html', {'user': user})
