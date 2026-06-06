"""
Agent 6 — Interview Question Generator

Creates tailored interview questions and answer
"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedResume, ParsedJD, InterviewQuestions

SYSTEM_PROMPT = """You are an expert interview coach and hiring manager.
Generate realistic, role-specific interview questions and practical answer tips
based on the candidate's background and the job description.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "technical": [
    "5 technical questions specific to the role's required skills and the candidate's gaps"
  ],
  "behavioral": [
    "5 STAR-method behavioral questions relevant to the role's responsibilities"
  ],
  "role_specific": [
    "5 questions a hiring manager would ask about the specific responsibilities in the JD"
  ],
  "suggested_answers_tips": [
    "5 practical tips for answering these questions effectively in an interview"
  ]
}

Rules:
- Questions must feel like they'd come from a real hiring manager for this exact role.
- Technical questions should probe the candidate's weaker or missing skills.
- Behavioral questions should reference scenarios relevant to the role.
- Answer tips should be concrete strategies, not generic advice.
"""


def run_interview_generator(resume: ParsedResume, jd: ParsedJD) -> InterviewQuestions:
    """
    Generate tailored interview questions and coaching tips.

    Args:
        resume: Structured resume data.
        jd: Structured JD data.

    Returns:
        InterviewQuestions: Technical, behavioral, and role-specific questions with tips.
    """
    recent_roles = [
        f"{e.title} at {e.company}" for e in resume.experience[:3]
    ]

    user_prompt = f"""
Target role: {jd.job_title}
Company: {jd.company}

Key responsibilities: {jd.responsibilities}
Required skills: {jd.required_skills}
Preferred skills: {jd.preferred_skills}

Candidate background:
- Skills: {resume.skills}
- Recent roles: {recent_roles}
- Education: {[f"{e.degree} from {e.institution}" for e in resume.education]}

Generate a comprehensive interview preparation kit.
"""
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return InterviewQuestions(**data)
