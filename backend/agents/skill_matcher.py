"""
Agent 3 — Skill Matcher

Compares the candidate's skills against JD requirements and computes a match percentage.
"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedResume, ParsedJD, SkillMatch

SYSTEM_PROMPT = """You are a precise skill matching engine.
Compare the candidate's skills and experience against the job requirements.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "matched_skills": ["skills the candidate clearly has that are required or preferred"],
  "missing_skills": ["required or preferred skills the candidate does not have"],
  "bonus_skills": ["candidate skills not mentioned in the JD but potentially valuable"],
  "match_percentage": 0.0
}

Rules:
- match_percentage is a float between 0.0 and 100.0 representing overall fit.
- Be strict: only mark a skill as matched if it clearly appears in the candidate's profile.
- Consider synonyms (e.g. 'React' matches 'ReactJS', 'ML' matches 'Machine Learning').
- Do not invent skills not present in either profile.
"""


def run_skill_matcher(resume: ParsedResume, jd: ParsedJD) -> SkillMatch:
    """
    Match candidate skills against JD requirements.

    Args:
        resume: Structured candidate data from the Resume Parser agent.
        jd: Structured JD data from the JD Analyser agent.

    Returns:
        SkillMatch: Matched, missing, bonus skills and overall match percentage.
    """
    experience_descriptions = [
        e.description for e in resume.experience
    ]

    user_prompt = f"""
Candidate skills listed: {resume.skills}
Candidate experience descriptions:
{chr(10).join(f'- {d}' for d in experience_descriptions)}

JD required skills: {jd.required_skills}
JD preferred skills: {jd.preferred_skills}
JD ATS keywords: {jd.keywords}

Perform a detailed skill match and compute the match percentage.
"""
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return SkillMatch(**data)
