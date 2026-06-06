"""
Agent 2 — JD Analyser

Extracts structured requirements from a raw job description using the LLM.
"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedJD

SYSTEM_PROMPT = """You are an expert job description analyst.
Extract all structured requirements from the job description provided.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "job_title": "string",
  "company": "string (or empty string if not mentioned)",
  "required_skills": ["must-have technical and soft skills"],
  "preferred_skills": ["nice-to-have / bonus skills"],
  "experience_required": "string e.g. '3-5 years of backend development'",
  "education_required": "string e.g. 'Bachelor in Computer Science or equivalent'",
  "responsibilities": ["key day-to-day responsibilities"],
  "keywords": ["important ATS keywords and phrases from the JD"]
}

Rules:
- Never omit any key.
- Use empty string "" for missing string fields.
- Use empty list [] for missing list fields.
- keywords should include all domain terms, tools, frameworks, and role-specific phrases
  that an ATS system might scan for.
"""


def run_jd_analyzer(jd_text: str) -> ParsedJD:
    """
    Analyse a raw job description into a structured ParsedJD object.

    Args:
        jd_text: Raw job description text pasted by the user.

    Returns:
        ParsedJD: Validated Pydantic model with all JD requirements.
    """
    user_prompt = f"Analyse the following job description:\n\n{jd_text}"
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return ParsedJD(**data)
