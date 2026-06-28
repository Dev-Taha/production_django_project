from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    path('preview/dark-1/', views.dark_template1_preview, name='preview_dark_1'),
    path('preview/dark-2/', views.dark_template2_preview, name='preview_dark_2'),
    path('preview/light-1/', views.light_template1_preview, name='preview_light_1'),
    path('preview/light-2/', views.light_template2_preview, name='preview_light_2'),
    path('step-one/', views.step_one, name='step_one'),
    path('step-two/', views.step_two, name='step_two'),
    path('step-three/', views.step_three, name='step_three'),
]
