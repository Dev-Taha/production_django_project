"""
portfolios/admin.py

Django admin lets you enter portfolio data immediately, no dashboard needed.
All related items appear as inlines on the Profile page.
"""
from django.contrib import admin
from .models import (
    Theme, Profile, ResearchInterest, Publication,
    Teaching, Education, ContactLink,
)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "template_path", "created_at")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)


# ─── Inlines on the Profile page ─────────────────────────────────────────────
class ResearchInterestInline(admin.TabularInline):
    model = ResearchInterest
    extra = 0
    fields = ("order_index", "title", "tags")


class EducationInline(admin.StackedInline):
    model = Education
    extra = 0
    fields = (
        ("degree", "field_of_study"),
        "institution",
        ("start_year", "end_year"),
        "description",
        "honor",
        "order_index",
    )


class PublicationInline(admin.StackedInline):
    model = Publication
    extra = 0
    fields = (
        "title",
        "authors",
        ("venue", "year", "pub_type"),
        ("pdf_link", "external_url", "code_link"),
        ("is_featured", "order_index"),
    )


class TeachingInline(admin.TabularInline):
    model = Teaching
    extra = 0
    fields = ("order_index", "course_code", "course_name", "term", "role", "syllabus_link")


class ContactLinkInline(admin.TabularInline):
    model = ContactLink
    extra = 0
    fields = ("order_index", "link_type", "label", "value", "url")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "academic_title", "institution", "theme", "is_published", "view_link")
    list_filter = ("is_published", "theme")
    search_fields = ("full_name", "user__email", "user__username", "institution")
    prepopulated_fields = {"slug": ("full_name",)}

    fieldsets = (
        ("Identity", {
            "fields": ("user", "full_name", "slug", "academic_title", "institution", "tagline"),
        }),
        ("Bio & status", {
            "fields": ("bio", "current_status"),
        }),
        ("Media", {
            "fields": ("profile_image", "cv_file"),
        }),
        ("Stats", {
            "fields": ("years_teaching", "citation_count", "students_supervised"),
            "classes": ("collapse",),
        }),
        ("Theme & visibility", {
            "fields": ("theme", "is_published"),
        }),
    )

    inlines = [
        ResearchInterestInline,
        EducationInline,
        PublicationInline,
        TeachingInline,
        ContactLinkInline,
    ]

    def view_link(self, obj):
        from django.utils.html import format_html
        if obj.is_published:
            return format_html('<a href="/u/{}/" target="_blank">View ↗</a>', obj.slug)
        return "—"
    view_link.short_description = "Public URL"
