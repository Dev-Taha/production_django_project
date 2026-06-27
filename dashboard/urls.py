from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.dashboard_view, name='main_dashboard'),
    path('templates/', views.templates_view, name='templates_dashboard'),
    path('settings/', views.settings_view, name='setting_dashboard'),
]