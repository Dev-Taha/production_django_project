"""
Run: python manage.py seed_demo

Creates a demo user 'ahmed' (password: demo1234) with a fully-populated
portfolio. Re-run anytime — it's idempotent (wipes & re-seeds related rows).
"""
import bcrypt

from django.core.management.base import BaseCommand

from accounts.models import User as UserModel
from portfolios.models import (
    Profile, Theme, ResearchInterest, Publication,
    Teaching, Education, ContactLink,
)


class Command(BaseCommand):
    help = "Seed a demo portfolio (Ahmed Ali)"

    def handle(self, *args, **options):
        try:
            theme = Theme.objects.get(slug="academic-light")
        except Theme.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "Theme 'academic-light' not found.\n"
                "Run first:  python manage.py sync_themes"
            ))
            return

        # User
        email = "ahmed.ali@example.edu"
        user, created = UserModel.objects.get_or_create(
            email=email,
            defaults={
                "first_name": "Ahmed",
                "last_name": "Ali",
                "password": bcrypt.hashpw("demo1234".encode(), bcrypt.gensalt()).decode(),
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created user 'ahmed' (password: demo1234)"))

        # Profile
        profile, _ = Profile.objects.update_or_create(
            user=user,
            defaults={
                "full_name": "Ahmed Ali",
                "slug": "ahmed-ali",
                "academic_title": "Professor of Computer Science",
                "institution": "University of Example · Department of Computer Science",
                "tagline": "Building language models that learn more from less.",
                "bio": (
                    "I work at the intersection of **machine learning** and **natural language processing**, "
                    "with a focus on building systems that learn efficiently from limited supervision. "
                    "My group studies how language models can be made more reliable, interpretable, "
                    "and useful to the people who depend on them.\n\n"
                    "Before joining the University of Example I completed my PhD at MIT and spent two years "
                    "at a research lab in Zürich. I teach courses on machine learning and NLP at both "
                    "undergraduate and graduate levels, and supervise a small group of doctoral students."
                ),
                "current_status": "On sabbatical at ETH Zürich, Spring 2026",
                "years_teaching": 15,
                "citation_count": 1200,
                "students_supervised": 12,
                "theme": theme,
                "is_published": True,
            },
        )

        # Wipe and re-seed related rows so the command is safely re-runnable
        profile.research_interests.all().delete()
        profile.publications.all().delete()
        profile.teachings.all().delete()
        profile.education_entries.all().delete()
        profile.contact_links.all().delete()

        # Research
        ResearchInterest.objects.bulk_create([
            ResearchInterest(profile=profile, order_index=0,
                title="Learning from limited supervision",
                description="How can models learn useful representations and behaviours from far less labelled data than current systems require? Recent work focuses on self-supervised pretraining, in-context learning, and the role of data curation in shaping what models acquire.",
                tags="few-shot learning, self-supervision, data curation"),
            ResearchInterest(profile=profile, order_index=1,
                title="Interpretability of language models",
                description="Methods for understanding what large language models compute internally, and how their behaviour can be predicted, audited, and edited. Active collaborations on mechanistic interpretability with researchers at several institutions.",
                tags="interpretability, mechanistic analysis, evaluation"),
            ResearchInterest(profile=profile, order_index=2,
                title="Reliable deployment of ML systems",
                description="Practical work on calibration, abstention, distribution shift, and human–AI collaboration in high-stakes domains such as clinical decision support and educational technology.",
                tags="reliability, calibration, human–AI interaction"),
        ])

        # Publications
        Publication.objects.bulk_create([
            Publication(profile=profile,
                title="Curriculum-aware pretraining for instruction-following language models",
                description="A new pretraining strategy for instruction-following models that balances task specificity with generalization.",
                pdf_link="https://example.com/p1.pdf",
                github_link="https://github.com/example/curriculum",
                publication_date="2025-06-01"),
            Publication(profile=profile,
                title="Calibrated abstention in question answering with retrieval",
                description="A study of abstention thresholds for retrieval-augmented QA systems.",
                pdf_link="https://example.com/p2.pdf",
                publication_date="2024-09-15"),
            Publication(profile=profile,
                title="A practitioner's guide to mechanistic interpretability",
                description="Practical techniques for inspecting and debugging modern language models.",
                pdf_link="https://example.com/p3.pdf",
                publication_date="2024-05-21"),
            Publication(profile=profile,
                title="Data-efficient transfer in clinical natural language understanding",
                description="An investigation into transfer learning for low-resource clinical NLP tasks.",
                pdf_link="https://example.com/p4.pdf",
                publication_date="2023-11-08"),
            Publication(profile=profile,
                title="On the geometry of in-context learning",
                description="Empirical and theoretical analysis of in-context learning dynamics.",
                pdf_link="https://example.com/p5.pdf",
                publication_date="2023-03-30"),
        ])

        # Teaching
        Teaching.objects.bulk_create([
            Teaching(profile=profile, order_index=0,
                course_name="Introduction to Machine Learning",
                semester="Fall 2025",
                description="Undergraduate introduction to supervised learning, optimization, and representation learning.",
                syllabus_link="https://example.com/cs447"),
            Teaching(profile=profile, order_index=1,
                course_name="Advanced Natural Language Processing",
                semester="Spring 2025",
                description="Graduate seminar on large language models, transformers, and responsible AI.",
                syllabus_link="https://example.com/cs621"),
            Teaching(profile=profile, order_index=2,
                course_name="Seminar: Interpretability in Modern Machine Learning",
                semester="Spring 2025",
                description="Student-led presentations exploring mechanistic interpretability techniques.",
                syllabus_link="https://example.com/cs498"),
            Teaching(profile=profile, order_index=3,
                course_name="Programming for Scientists",
                semester="Fall 2024",
                description="Hands-on Python programming for scientific research and data analysis.",
            ),
        ])

        # Education
        Education.objects.bulk_create([
            Education(profile=profile, order_index=0,
                degree="Ph.D.", field_of_study="in Computer Science",
                institution="Massachusetts Institute of Technology",
                start_year=2015, end_year=2020,
                description="Dissertation: Sample-efficient learning of structured representations for natural language understanding\nAdvisor: Prof. Jane Rosenberg",
                honor="Outstanding Dissertation Award"),
            Education(profile=profile, order_index=1,
                degree="M.Sc.", field_of_study="in Computer Science",
                institution="Stanford University",
                start_year=2013, end_year=2015,
                description="Concentration: Artificial Intelligence and Machine Learning"),
            Education(profile=profile, order_index=2,
                degree="B.Sc.", field_of_study="in Computer Science",
                institution="University of Cairo",
                start_year=2009, end_year=2013,
                description="Minor: Mathematics",
                honor="Summa Cum Laude"),
        ])

        # Contact
        ContactLink.objects.bulk_create([
            ContactLink(profile=profile, order_index=0, link_type="email",
                label="Email", value="ahmed.ali@example.edu", url="mailto:ahmed.ali@example.edu"),
            ContactLink(profile=profile, order_index=1, link_type="location",
                label="Office", value="Building 4, Room 312"),
            ContactLink(profile=profile, order_index=2, link_type="clock",
                label="Office hours", value="Tuesdays 14:00–16:00, or by appointment"),
            ContactLink(profile=profile, order_index=3, link_type="scholar",
                label="Google Scholar", value="scholar.google.com/ahmedali", url="https://scholar.google.com/"),
            ContactLink(profile=profile, order_index=4, link_type="github",
                label="GitHub", value="github.com/ahmedali", url="https://github.com/"),
            ContactLink(profile=profile, order_index=5, link_type="orcid",
                label="ORCID", value="0000-0000-0000-0000", url="https://orcid.org/"),
        ])

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Demo portfolio seeded.\n"
            f"  Public URL:  http://127.0.0.1:8000/u/{profile.slug}/\n"
            f"  Admin login: ahmed / demo1234"
        ))
