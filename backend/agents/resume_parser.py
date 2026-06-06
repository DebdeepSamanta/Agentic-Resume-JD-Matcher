"""
Agent 1 — Resume Parser

Extracts structured candidate data from raw resume text using the LLM.
"""
from backend.services.llm import call_llm_json
from backend.schemas.output import ParsedResume

SYSTEM_PROMPT = """You are an expert resume parser.
Extract structured information from the resume text provided.

Return ONLY a valid JSON object — no commentary, no markdown fences. Use this exact schema:
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "location": "string",
  "summary": "string (professional summary or empty string if absent)",
  "skills": ["list", "of", "technical and soft skills"],
  "experience": [
    {
      "title": "job title",
      "company": "company name",
      "duration": "e.g. Jan 2020 - Mar 2023",
      "description": "role description and key achievements"
    }
  ],
  "education": [
    {
      "degree": "e.g. B.Tech Computer Science",
      "institution": "university / college name",
      "year": "graduation year or range"
    }
  ],
  "certifications": ["list of certifications or empty list"],
  "languages": ["list of spoken languages or empty list"]
}

Rules:
- Never omit any key.
- Use empty string "" for missing string fields.
- Use empty list [] for missing list fields.
- Do not invent information not present in the resume.
"""


def run_resume_parser(resume_text: str) -> ParsedResume:
    """
    Parse raw resume text into a structured ParsedResume object.

    Args:
        resume_text: Plain text extracted from the candidate's resume PDF.

    Returns:
        ParsedResume: Validated Pydantic model with all candidate details.
    """
    user_prompt = f"Parse the following resume:\n\n{resume_text}"
    data = call_llm_json(SYSTEM_PROMPT, user_prompt)
    return ParsedResume(**data)
