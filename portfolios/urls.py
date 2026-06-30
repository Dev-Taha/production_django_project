"""
portfolios/urls.py
"""
from django.urls import path

from . import views

app_name = "portfolios"

urlpatterns = [
    # Public portfolio at /u/<slug>/
    path("u/<slug:slug>/", views.portfolio_detail, name="detail"),
    path("preview/<slug:theme_slug>/", views.portfolio_preview, name="preview"),
    path('onboarding-one/', views.onboarding_one, name='onboarding_one'),
    path('onboarding-two/', views.onboarding_two, name='onboarding_two'),
    path('onboarding-three/', views.onboarding_three, name='onboarding_three'),
    path('preview/dark-1/', views.dark_template1_preview, name='preview_dark_1'),
    path('preview/dark-2/', views.dark_template2_preview, name='preview_dark_2'),
    path('preview/light-1/', views.light_template1_preview, name='preview_light_1'),
    path('preview/light-2/', views.light_template2_preview, name='preview_light_2'),
    
]
