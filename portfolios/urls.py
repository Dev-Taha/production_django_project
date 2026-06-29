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
]
