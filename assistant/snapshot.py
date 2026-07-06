def build_snapshot(profile):
    """
    Collects everything the assistant is allowed to know about a user
    into one plain dict. This is the ONLY user data the AI ever sees.
    """

    """The ONLY user data the AI ever sees."""
    interests = [
        {"title": ri.title, "has_description": bool(ri.description), "tags": ri.tag_list}
        for ri in profile.research_interests_entries.all()
    ]
    # Legacy fallback: free-text field, comma-separated
    if not interests and profile.research_interests:
        interests = [{"title": t.strip(), "has_description": False, "tags": []}
                     for t in profile.research_interests.split(",") if t.strip()]

    contact_types = set(profile.contact_links.values_list("link_type", flat=True))

    return {
        "profile": {
            "full_name": profile.full_name,
            "academic_title": profile.academic_title,
            "institution": profile.institution,
            "tagline": profile.tagline,
            "bio": profile.bio,
            "bio_word_count": len(profile.bio.split()) if profile.bio else 0,
            "has_photo": bool(profile.profile_image),
            "has_cv": bool(profile.cv_file),
            "has_scholar": bool(profile.google_scholar),
        },
        "contact": {
            "types_present": sorted(contact_types),
            "has_email": "email" in contact_types,
            "has_orcid": "orcid" in contact_types,
            "link_count": profile.contact_links.count(),
        },
        "research_interests": interests,
        "education": [
            {"degree": e.degree, "institution": e.institution,
             "start_year": e.start_year, "end_year": e.end_year,
             "has_description": bool(e.description)}
            for e in profile.education_entries.all()
        ],
        "teaching": [
            {"course_name": t.course_name, "semester": t.semester,
             "has_description": bool(t.description), "has_syllabus": bool(t.syllabus_link)}
            for t in profile.teachings.all()
        ],
        "publications": [
            {"title": p.title,
             "year": p.publication_date.year if p.publication_date else None,
             "has_description": bool(p.description),
             "has_link": bool(p.pdf_link) or bool(p.github_link)}
            for p in profile.publications.all()
        ],
    }