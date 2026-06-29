
from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from portfolios.models import Theme, Profile


def dashboard_view(request):
        if 'user_id' not in request.session:
            return redirect('accounts:login')
        user = User.objects.get(id=request.session['user_id'])

        return render(request, 'dashboard/dashboard.html', {'user': user})


def templates_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')

    user = User.objects.get(id=request.session['user_id'])

    # Ensure this user has a Profile row (auto-create on first visit)
    default_theme = Theme.objects.filter(slug='academic-light', is_active=True).first()
    full_name = (
            getattr(user, 'full_name', None)
            or f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            or getattr(user, 'username', None)
            or getattr(user, 'email', 'User')
    )
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={'full_name': full_name, 'theme': default_theme},
    )

    # All active themes for the gallery
    themes = Theme.objects.filter(is_active=True).order_by('name')

    # Which theme is shown in the preview pane right now
    preview_slug = request.GET.get('preview')
    active_theme = None
    if preview_slug:
        active_theme = Theme.objects.filter(slug=preview_slug, is_active=True).first()
    active_theme = active_theme or profile.theme or themes.first()

    preview_url = None
    if active_theme:
        preview_url = reverse('portfolios:preview', args=[active_theme.slug])

    print(
        f">>> DEBUG: active_theme={active_theme}, slug={active_theme.slug if active_theme else None}, preview_url={preview_url}")



    return render(request, 'dashboard/templates_dashboard.html', {
        'user': user,
        'profile': profile,
        'themes': themes,
        'active_theme': active_theme,
        'preview_url': preview_url,
    })

def settings_view(request):
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'dashboard/setting_dashboard.html', {'user': user})

def set_theme_view(request):
    """Save & Publish — sets the selected theme as the user's active theme."""
    if 'user_id' not in request.session:
        return redirect('accounts:login')
    if request.method != 'POST':
        return redirect('dashboard:templates_dashboard')

    user = User.objects.get(id=request.session['user_id'])
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'full_name': user.username})

    slug = request.POST.get('theme_slug')
    theme = get_object_or_404(Theme, slug=slug, is_active=True)
    profile.theme = theme
    profile.save()

    return redirect('dashboard:templates_dashboard')