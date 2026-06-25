
from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
import bcrypt

def login(request):
  
    if 'user_id' in request.session: 
        return redirect('dashboard:main_dashboard')
    context = {'login_form': LoginForm()}

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email_input = login_form.cleaned_data['email']
            password_input = login_form.cleaned_data['password']
            user_list = User.objects.filter(email__iexact=email_input)
            
            if user_list:
                logged_user = user_list[0]
                if bcrypt.checkpw(password_input.encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    return redirect('dashboard:main_dashboard')
            
            messages.error(request, "Invalid Email or Password")
            
            context['login_form'] = login_form
            
        else:
            context['login_form'] = login_form

    
    return render(request, 'accounts/login.html', context)

def register(request):

    if 'user_id' in request.session:
        return redirect('dashboard:main_dashboard')
 
    context = {'reg_form': RegisterForm()}

    if request.method == 'POST':
        reg_form = RegisterForm(request.POST) 
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            password = reg_form.cleaned_data['password']
            user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.save()
            
            request.session['user_id'] = user.id 
            return redirect('dashboard:main_dashboard')
        
        context['reg_form'] = reg_form

    return render(request, 'accounts/register.html', context)

def logout(request):
    request.session.clear()
    messages.info(request, "You have been logged out successfully.")
    return redirect('accounts:login') 





