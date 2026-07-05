def build_snapshot(profile):
    """
    Collects everything the assistant is allowed to know about a user
    into one plain dict. This is the ONLY user data the AI ever sees.
    """
    return {
        "profile": {
            "full_name": profile.full_name,
            "academic_title": profile.academic_title,
            "bio": profile.bio,
            "bio_word_count": len(profile.bio.split()) if profile.bio else 0,
            "has_photo": bool(profile.profile_image),          # adjust to your field names
        },
        "publications": [
            {
                "title": p.title,
                "year": p.publication_date.year if p.publication_date else None,
                "has_pdf": bool(p.pdf_link),
            }
            for p in profile.publications.all()      # adjust related_name
        ],
        "teaching": [
            {"course_name": t.course_name, "has_description": bool(t.description)}
            for t in profile.teachings.all()
        ],
    }