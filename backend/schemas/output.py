from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


# ── Resume ────────────────────────────────────────────────────────────────────

class ExperienceEntry(BaseModel):
    title: str
    company: str
    duration: str
    description: str


class EducationEntry(BaseModel):
    degree: str
    institution: str
    year: str


class ParsedResume(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    summary: str
    skills: list[str]
    experience: list[ExperienceEntry]
    education: list[EducationEntry]
    certifications: list[str]
    languages: list[str]


# ── Job Description ───────────────────────────────────────────────────────────

class ParsedJD(BaseModel):
    job_title: str
    company: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_required: str
    education_required: str
    responsibilities: list[str]
    keywords: list[str]


# ── Skill Match ───────────────────────────────────────────────────────────────

class SkillMatch(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    bonus_skills: list[str]
    match_percentage: float


# ── ATS Score ─────────────────────────────────────────────────────────────────

class ATSScore(BaseModel):
    overall_score: int
    keyword_score: int
    format_score: int
    experience_score: int
    education_score: int
    breakdown: dict[str, str]


# ── Recommendations ───────────────────────────────────────────────────────────

class Recommendation(BaseModel):
    summary_suggestions: list[str]
    skills_to_add: list[str]
    experience_gaps: list[str]
    quick_wins: list[str]
    long_term_actions: list[str]


# ── Interview Questions ───────────────────────────────────────────────────────

class InterviewQuestions(BaseModel):
    technical: list[str]
    behavioral: list[str]
    role_specific: list[str]
    suggested_answers_tips: list[str]


# ── Final Report ──────────────────────────────────────────────────────────────

class FinalReport(BaseModel):
    parsed_resume: ParsedResume
    parsed_jd: ParsedJD
    skill_match: SkillMatch
    ats_score: ATSScore
    recommendations: Recommendation
    interview_questions: InterviewQuestions


# ── API Response ──────────────────────────────────────────────────────────────

class AnalysisResponse(BaseModel):
    success: bool
    report: Optional[FinalReport] = None
    error: Optional[str] = None


class MatchRequest(BaseModel):
    resume_text: str = Field(..., description="Raw resume text")
    job_description: str = Field(..., description="Job description text")
