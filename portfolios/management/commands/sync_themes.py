"""
Run: python manage.py sync_themes

Scans templates/themes/<slug>/ folders for theme.json files and upserts
each one into the Theme table. Adding a new theme = drop a folder + re-run this.
"""
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolios.models import Theme


class Command(BaseCommand):
    help = "Sync themes from templates/themes/ folders into the Theme table"

    def handle(self, *args, **options):
        themes_dir = Path(settings.BASE_DIR) / "templates" / "themes"

        if not themes_dir.exists():
            self.stdout.write(self.style.ERROR(f"Themes dir not found: {themes_dir}"))
            return

        count = 0
        for folder in sorted(themes_dir.iterdir()):
            if not folder.is_dir():
                continue

            meta_file = folder / "theme.json"
            if not meta_file.exists():
                self.stdout.write(self.style.WARNING(f"  skip {folder.name}/ (no theme.json)"))
                continue

            try:
                with open(meta_file) as f:
                    meta = json.load(f)
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"  bad JSON in {folder.name}/theme.json: {e}"))
                continue

            theme, created = Theme.objects.update_or_create(
                slug=meta["slug"],
                defaults={
                    "name": meta["name"],
                    "description": meta.get("description", ""),
                    "template_path": f"themes/{folder.name}/index.html",
                    "preview_image": f"themes/{folder.name}/{meta.get('preview_image', 'preview.png')}",
                    "palette": meta.get("palette", {}),
                    "is_active": meta.get("is_active", True),
                },
            )
            verb = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"  {verb}: {theme.name} ({theme.slug})"))
            count += 1

        self.stdout.write(self.style.SUCCESS(f"\nSynced {count} theme(s)."))
