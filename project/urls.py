from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from portfolios import views as portfolios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('portfolios/', include('portfolios.urls')),
    path("assistant/", include("assistant.urls")),
    path('api/onboarding/upload-cv/', portfolios_views.upload_cv, name='upload_cv'),
    path('api/onboarding/cv-status/<str:task_id>/', portfolios_views.cv_status, name='cv_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
