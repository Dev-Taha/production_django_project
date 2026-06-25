from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import User


class Landing(generic.TemplateView):
    template_name = 'dashboard/dashboard.html'
    # template_name = 'dashboard/landing.html'

def dashboard_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    user = User.objects.get(id=request.session['user_id'])
    
    return render(request, 'dashboard/dashboard.html', {'user': user})
  
    