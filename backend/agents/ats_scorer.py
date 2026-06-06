"""
Agent 4 — ATS Scorer

Computes a multi-dimensional ATS (Applicant Tracking System) score

"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedResume, ParsedJD, SkillMatch, ATSScore

SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) scoring engine.
Score the candidate's resume against the job description across four dimensions.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "overall_score": 0,
  "keyword_score": 0,
  "format_score": 0,
  "experience_score": 0,
  "education_score": 0,
  "breakdown": {
    "keywords": "short comment on keyword density and relevance",
    "format": "comment on resume structure, sections, and readability",
    "experience": "comment on how well experience aligns with role requirements",
    "education": "comment on education match against JD requirements"
  }
}

Scoring rules:
- All scores are integers between 0 and 100.
- overall_score = weighted composite:
    keyword_score × 0.35 + experience_score × 0.35 + education_score × 0.15 + format_score × 0.15
- Round overall_score to the nearest integer.
- breakdown comments should be 1-2 concise sentences each.
"""


def run_ats_scorer(
    resume: ParsedResume,
    jd: ParsedJD,
    skill_match: SkillMatch,
) -> ATSScore:
    """
    Compute ATS scores for the candidate against the job description.

    Args:
        resume: Structured resume data.
        jd: Structured JD data.
        skill_match: Output from the Skill Matcher agent.

    Returns:
        ATSScore: Scores per dimension plus a breakdown of comments.
    """
    user_prompt = f"""
Resume overview:
- Skills listed: {resume.skills}
- Number of experience entries: {len(resume.experience)}
- Education: {[f"{e.degree} from {e.institution}" for e in resume.education]}
- Certifications: {resume.certifications}
- Has professional summary: {bool(resume.summary.strip())}

JD requirements:
- Required skills: {jd.required_skills}
- ATS keywords: {jd.keywords}
- Experience required: {jd.experience_required}
- Education required: {jd.education_required}

Skill match results:
- Matched skills: {skill_match.matched_skills}
- Missing skills: {skill_match.missing_skills}
- Overall skill match %: {skill_match.match_percentage}

Compute the ATS score breakdown.
"""
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return ATSScore(**data)
