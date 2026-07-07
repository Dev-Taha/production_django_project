"""
portfolios/models.py

All portfolio-related models. Architecture: skeleton templates live on disk;
this DB only stores data + a pointer (template_path) to the right theme folder.
"""
import re

from django.db import models
from django.utils.text import slugify
from accounts.models import User


class Theme(models.Model):
    slug = models.SlugField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    template_path = models.CharField(
        max_length=255,
        help_text="Path relative to TEMPLATES dirs, e.g. 'themes/academic-light/index.html'",
    )
    preview_image = models.CharField(max_length=255, blank=True)
    palette = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Identity
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=120, blank=True)
    academic_title = models.CharField(max_length=255, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    field_of_study = models.CharField(max_length=255, blank=True)
    tagline = models.CharField(max_length=255, blank=True)

    # Bio
    bio = models.TextField(blank=True, help_text="Use double newlines for paragraphs. Wrap emphasis in **bold**.")
    current_status = models.CharField(max_length=140, blank=True, help_text="e.g. 'On sabbatical at ETH, Spring 2026'")

    # Media
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)

    google_scholar = models.URLField(blank=True, null=True)
    research_gate = models.URLField(blank=True, null=True)

    # Stats (manual for now; can derive later)
    years_teaching = models.PositiveIntegerField(blank=True, null=True)
    citation_count = models.PositiveIntegerField(blank=True, null=True)
    students_supervised = models.PositiveIntegerField(blank=True, null=True)

    # Theme & visibility
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    # Template choice (selectable template skin, separate from `theme`)
    TEMPLATE_CLASSIC = 'classic-scholar'
    TEMPLATE_MODERN = 'modern-dark'
    TEMPLATE_MINIMAL = 'minimalist-lab'
    TEMPLATE_EXECUTIVE = 'executive-academic'

    TEMPLATE_CHOICES = [
        (TEMPLATE_CLASSIC, 'Classic Scholar'),
        (TEMPLATE_MODERN, 'Modern Dark'),
        (TEMPLATE_MINIMAL, 'Minimalist Lab'),
        (TEMPLATE_EXECUTIVE, 'Executive Academic'),
    ]

    selected_template = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        blank=True,
        null=True,
        default=TEMPLATE_CLASSIC,
    )

    research_interests = models.TextField(blank=True, default='')
    onboarding_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name) or f"user-{self.user_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.get_username()

    @property
    def profile_picture(self):
        return self.profile_image

    @property
    def bio_paragraphs(self):
        """Split bio on blank lines and convert **bold** → <strong> for template rendering."""
        if not self.bio:
            return []
        paras = [p.strip() for p in self.bio.split("\n\n") if p.strip()]
        return [re.sub(r"\*\*(.+?)\*\*", r"<em>\1</em>", p) for p in paras]

    @property
    def publications_count(self):
        return self.publications.count()


class ResearchInterest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="research_interests_entries")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order_index"]

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="publications")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pdf_link = models.TextField(blank=True)
    github_link = models.CharField(max_length=500, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title


class Teaching(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="teachings")
    course_name = models.CharField(max_length=45)
    description = models.TextField(blank=True)
    syllabus_link = models.URLField(blank=True, null=True)
    semester = models.CharField(max_length=45, blank=True)
    def __str__(self):
        return self.course_name


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="education_entries")
    degree = models.CharField(max_length=100, help_text="e.g. 'Ph.D.', 'M.Sc.', 'B.Sc.'")
    field_of_study = models.CharField(max_length=255, blank=True, help_text="e.g. 'in Computer Science'")
    institution = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True, help_text="Leave blank if ongoing")
    description = models.TextField(blank=True, help_text="Dissertation title, advisor, concentration, minor...")
    honor = models.CharField(max_length=100, blank=True, help_text="Award badge (optional)")
    order_index = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_year"]
        verbose_name_plural = "Education entries"

    def __str__(self):
        return f"{self.degree} — {self.institution}"

    @property
    def description_lines(self):
        return [l.strip() for l in self.description.split("\n") if l.strip()]


class ContactLink(models.Model):
    LINK_TYPES = [
        ("email", "Email"),
        ("location", "Location"),
        ("phone", "Phone"),
        ("clock", "Office Hours"),
        ("scholar", "Google Scholar"),
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("orcid", "ORCID"),
        ("website", "Website"),
        ("link", "Other Link"),
    ]

    ICON_MAP = {
        "email": "bi-envelope",
        "location": "bi-geo-alt",
        "phone": "bi-telephone",
        "clock": "bi-clock",
        "scholar": "bi-mortarboard",
        "github": "bi-github",
        "linkedin": "bi-linkedin",
        "orcid": "bi-person-badge",
        "website": "bi-globe",
        "link": "bi-link-45deg",
    }

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contact_links")
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default="link")
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order_index"]

    def __str__(self):
        return f"{self.label}: {self.value}"

    @property
    def icon_class(self):
        return self.ICON_MAP.get(self.link_type, "bi-link-45deg")