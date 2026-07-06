from dataclasses import dataclass
from datetime import date

@dataclass
class Finding:
    section: str      # "biography", "publications", ...
    status: str       # "ok" | "weak" | "missing" | "inconsistent"
    points: float     # earned
    max_points: float # possible
    message: str      # human-readable, also shown to the AI later


# Section weights — must sum to 100
WEIGHTS = {
    "biography": 15,
    "publications": 20,
    "teaching": 15,
    "education": 15,
    "research_interests": 10,
    "contact": 10,
    "profile_basics": 10,
    "cv": 5,
}

def check_biography(snapshot) -> list[Finding]:
    w = WEIGHTS["biography"]
    words = snapshot["profile"]["bio_word_count"]

    if words == 0:
        return [Finding("biography", "missing", 0, w,
                "No biography. A 100-200 word bio is the most-read section of a portfolio.")]
    if words < 50:
        return [Finding("biography", "weak", w * 0.5, w,
                f"Biography is only {words} words. Aim for 100-200 words.")]
    return [Finding("biography", "ok", w, w, f"Biography present ({words} words).")]

def check_publications(snapshot) -> list[Finding]:
    w = WEIGHTS["publications"]
    pubs = snapshot["publications"]
    if not pubs:
        return [Finding("publications", "missing", 0, w,
                "No publications listed. Even preprints strengthen a profile.")]
    findings = []
    hits = sum((p["year"] is not None) + p["has_description"] + p["has_link"] for p in pubs)
    quality = hits / (len(pubs) * 3)
    pts = round(w * (0.6 + 0.4 * quality), 1)
    status = "ok" if quality >= 0.85 else "weak"
    findings.append(Finding("publications", status, pts, w,
        f"{len(pubs)} publication(s); metadata {round(quality*100)}% complete (date, description, link)."))
    for p in pubs:
        if p["year"] and p["year"] > date.today().year:
            findings.append(Finding("publications", "inconsistent", 0, 0,
                f"'{p['title'][:60]}' has a future date ({p['year']})."))
    return findings

def analyze(snapshot) -> dict:
    findings = [
        *check_biography(snapshot),
        *check_publications(snapshot),
        *check_teaching(snapshot),
        *check_education(snapshot),
        *check_research_interests(snapshot),
        *check_contact(snapshot),
        *check_profile_basics(snapshot),
        *check_cv(snapshot),
    ]
    score = min(100, round(sum(f.points for f in findings)))

    if score >= 90:   grade = "Excellent"
    elif score >= 75: grade = "Strong"
    elif score >= 55: grade = "Developing"
    elif score >= 35: grade = "Basic"
    else:             grade = "Incomplete"

    return {
        "completeness_score": score,
        "grade": grade,
        "findings": [vars(f) for f in findings],
    }

def check_education(snapshot) -> list[Finding]:
    w = WEIGHTS["education"]
    edu = snapshot["education"]
    if not edu:
        return [Finding("education", "missing", 0, w,
                "No education history. Add at least your highest degree.")]
    findings = [Finding("education", "ok", w, w,
                f"{len(edu)} education entr{'y' if len(edu)==1 else 'ies'} listed.")]
    for e in edu:
        if e["end_year"] and e["end_year"] < e["start_year"]:
            findings.append(Finding("education", "inconsistent", 0, 0,
                f"'{e['degree']} — {e['institution']}' ends ({e['end_year']}) before it starts ({e['start_year']})."))
    return findings


def check_research_interests(snapshot) -> list[Finding]:
    w = WEIGHTS["research_interests"]
    n = len(snapshot["research_interests"])
    if n == 0:
        return [Finding("research_interests", "missing", 0, w,
                "No research interests. Add 3-6 — they drive discoverability.")]
    if n < 3:
        return [Finding("research_interests", "weak", w * 0.5, w,
                f"Only {n} research interest(s). Aim for 3-6.")]
    return [Finding("research_interests", "ok", w, w, f"{n} research interests listed.")]


def check_contact(snapshot) -> list[Finding]:
    w = WEIGHTS["contact"]
    c = snapshot["contact"]
    findings, pts = [], 0.0
    if c["has_email"]:
        pts += w * 0.4
    else:
        findings.append(Finding("contact", "missing", 0, 0, "No contact email link."))
    if c["has_orcid"]:
        pts += w * 0.3
    else:
        findings.append(Finding("contact", "missing", 0, 0,
                        "No ORCID iD — the standard academic identifier, free at orcid.org."))
    if c["link_count"] >= 2:
        pts += w * 0.3
    findings.append(Finding("contact", "ok" if pts == w else "weak", round(pts, 1), w,
                    "Contact section complete." if pts == w else "Contact section partially complete."))
    return findings


def check_profile_basics(snapshot) -> list[Finding]:
    w = WEIGHTS["profile_basics"]
    p = snapshot["profile"]
    findings, pts = [], 0.0
    for field, share, msg in (("academic_title", 0.35, "No academic title."),
                              ("institution", 0.35, "No institution listed."),
                              ("has_photo", 0.30, "No profile photo uploaded.")):
        if p[field]:
            pts += w * share
        else:
            findings.append(Finding("profile_basics", "missing", 0, 0, msg))
    findings.append(Finding("profile_basics", "ok" if round(pts, 1) == w else "weak",
                    round(pts, 1), w,
                    "Profile basics complete." if round(pts, 1) == w else "Profile basics partially complete."))
    return findings


def check_cv(snapshot) -> list[Finding]:
    w = WEIGHTS["cv"]
    if snapshot["profile"]["has_cv"]:
        return [Finding("cv", "ok", w, w, "CV uploaded.")]
    return [Finding("cv", "missing", 0, w, "No CV uploaded.")]

def check_teaching(snapshot) -> list[Finding]:
    w = WEIGHTS["teaching"]
    teaching = snapshot["teaching"]
    if not teaching:
        return [Finding("teaching", "missing", 0, w,
                "No courses listed. Add the courses you teach with a short description.")]
    described = sum(1 for t in teaching if t["has_description"])
    ratio = described / len(teaching)
    pts = round(w * (0.7 + 0.3 * ratio), 1)
    status = "ok" if ratio >= 0.5 else "weak"
    msg = (f"{len(teaching)} course(s) listed."
           if status == "ok" else
           f"{len(teaching)} course(s) listed but most lack descriptions.")
    return [Finding("teaching", status, pts, w, msg)]
