"""
Agent 5 — Recommender

Generates personalised, actionable career coaching recommendations
based on the candidate's profile and the ATS analysis.
"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedResume, ParsedJD, SkillMatch, ATSScore, Recommendation

SYSTEM_PROMPT = """You are a senior career coach and resume strategist.
Provide specific, actionable recommendations to help the candidate improve
their resume and career profile for the target role.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "summary_suggestions": ["specific ways to rewrite or strengthen the professional summary"],
  "skills_to_add": ["skills to learn or add to the resume for a better match"],
  "experience_gaps": ["areas where the candidate's experience is thin or missing"],
  "quick_wins": ["easy edits the candidate can make today to immediately boost their ATS score"],
  "long_term_actions": ["career development steps for the next 3-12 months"]
}

Rules:
- Be specific and reference the actual JD and resume content.
- Avoid generic advice like "improve your resume". Be concrete.
- quick_wins should be actionable within 1 day (e.g. add a keyword, reword a bullet).
- Each list should contain 4-6 items.
"""


def run_recommender(
    resume: ParsedResume,
    jd: ParsedJD,
    skill_match: SkillMatch,
    ats_score: ATSScore,
) -> Recommendation:
    """
    Generate personalised recommendations for the candidate.

    Args:
        resume: Structured resume data.
        jd: Structured JD data.
        skill_match: Skill match results.
        ats_score: ATS scoring results.

    Returns:
        Recommendation: Categorised list of improvement suggestions.
    """
    recent_roles = [
        f"{e.title} at {e.company}" for e in resume.experience[:3]
    ]

    user_prompt = f"""
Target role: {jd.job_title} at {jd.company}

Candidate snapshot:
- Name: {resume.name}
- Current skills: {resume.skills}
- Recent experience: {recent_roles}
- Current summary: "{resume.summary}"

Gap analysis:
- Missing skills: {skill_match.missing_skills}
- ATS overall score: {ats_score.overall_score}/100
- Keyword score: {ats_score.keyword_score}/100
- Experience score: {ats_score.experience_score}/100
- ATS keyword comments: {ats_score.breakdown.get('keywords', '')}
- ATS experience comments: {ats_score.breakdown.get('experience', '')}

JD keywords to target: {jd.keywords}
JD responsibilities: {jd.responsibilities}

Generate targeted, specific recommendations.
"""
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return Recommendation(**data)
