from django.test import TestCase

from .views import resolve_preview_theme


class PortfolioPreviewTests(TestCase):
    def test_legacy_preview_alias_maps_to_existing_theme(self):
        theme = resolve_preview_theme("light-1")

        self.assertEqual(theme.slug, "academic-light")
        self.assertEqual(theme.template_path, "themes/academic-light/index.html")
