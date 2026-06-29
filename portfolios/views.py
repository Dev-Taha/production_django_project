"""
portfolios/views.py

Public portfolio view. Loads the user's data, then renders the template path
stored on their chosen Theme. Same view handles every theme — the template
swaps based on theme.template_path.
"""
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Profile, Theme

from django.views.decorators.clickjacking import xframe_options_sameorigin

def _render_portfolio(request, profile, theme=None, preview_mode=False):
    """Shared rendering logic for detail + preview."""
    theme = theme or profile.theme
    if not theme:
        raise Http404("No theme selected.")
    context = {
        "profile": profile,
        "research_interests": profile.research_interests.all(),
        "publications": profile.publications.all(),
        "teachings": profile.teachings.all(),
        "education": profile.education_entries.all(),
        "contact_links": profile.contact_links.all(),
        "preview_mode": preview_mode,
        "active_theme": theme,
    }
    return render(request, theme.template_path, context)


def portfolio_detail(request, slug):
    """Public portfolio page — /portfolios/u/<slug>/"""
    profile = get_object_or_404(Profile, slug=slug, is_published=True)
    return _render_portfolio(request, profile)

@xframe_options_sameorigin
def portfolio_preview(request, theme_slug):
    """
    Preview endpoint — /portfolios/preview/<theme_slug>/

    Loads the session-authenticated user's profile (if any), otherwise the
    demo profile, then renders it with the specified theme. Used by the
    Live Preview iframe in the dashboard.
    """
    theme = get_object_or_404(Theme, slug=theme_slug, is_active=True)

    profile = None
    user_id = request.session.get("user_id")
    if user_id:
        profile = Profile.objects.filter(user_id=user_id).first()

    if profile is None:
        profile = Profile.objects.filter(slug="ahmed-ali").first()

    if profile is None:
        raise Http404("No portfolio data available to preview.")

    return _render_portfolio(request, profile, theme=theme, preview_mode=True)
