"""
Run: python manage.py seed_demo

Creates a demo user 'ahmed' (password: demo1234) with a fully-populated
portfolio. Re-run anytime — it's idempotent (wipes & re-seeds related rows).
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from portfolios.models import (
    Profile, Theme, ResearchInterest, Publication,
    Teaching, Education, ContactLink,
)

User = get_user_model()


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
        user, created = User.objects.get_or_create(
            username="ahmed",
            defaults={"email": "ahmed.ali@example.edu", "first_name": "Ahmed", "last_name": "Ali"},
        )
        if created:
            user.set_password("demo1234")
            user.save()
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
            Publication(profile=profile, year=2025, is_featured=True,
                title="Curriculum-aware pretraining for instruction-following language models",
                authors="Chen, L., **Ali, A.**, Park, S., & Tanaka, R.",
                venue="Proceedings of NeurIPS 2025",
                pdf_link="https://example.com/p1.pdf",
                external_url="https://arxiv.org/abs/2025.00001",
                code_link="https://github.com/example/curriculum"),
            Publication(profile=profile, year=2024,
                title="Calibrated abstention in question answering with retrieval",
                authors="**Ali, A.**, & Rosenberg, D.",
                venue="Transactions of the Association for Computational Linguistics, 12, 891–908",
                pdf_link="https://example.com/p2.pdf"),
            Publication(profile=profile, year=2024,
                title="A practitioner's guide to mechanistic interpretability",
                authors="Park, S., **Ali, A.**, Chen, L., & Williams, J.",
                venue="Proceedings of ICML 2024",
                pdf_link="https://example.com/p3.pdf",
                external_url="https://arxiv.org/abs/2024.00001"),
            Publication(profile=profile, year=2023,
                title="Data-efficient transfer in clinical natural language understanding",
                authors="**Ali, A.**, Tanaka, R., & Wood, E.",
                venue="Journal of the American Medical Informatics Association, 30(8), 1422–1435",
                pdf_link="https://example.com/p4.pdf"),
            Publication(profile=profile, year=2023,
                title="On the geometry of in-context learning",
                authors="Wood, E., **Ali, A.**, & Chen, L.",
                venue="Proceedings of ICLR 2023 (Spotlight)",
                pdf_link="https://example.com/p5.pdf",
                external_url="https://arxiv.org/abs/2023.00001"),
        ])

        # Teaching
        Teaching.objects.bulk_create([
            Teaching(profile=profile, order_index=0,
                course_code="CS-447", course_name="Introduction to Machine Learning",
                term="Fall 2025", role="instructor", syllabus_link="https://example.com/cs447"),
            Teaching(profile=profile, order_index=1,
                course_code="CS-621", course_name="Advanced Natural Language Processing",
                term="Spring 2025", role="instructor", syllabus_link="https://example.com/cs621"),
            Teaching(profile=profile, order_index=2,
                course_code="CS-498", course_name="Seminar: Interpretability in Modern Machine Learning",
                term="Spring 2025", role="co_instructor", syllabus_link="https://example.com/cs498"),
            Teaching(profile=profile, order_index=3,
                course_code="CS-101", course_name="Programming for Scientists",
                term="Fall 2024", role="instructor"),
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
