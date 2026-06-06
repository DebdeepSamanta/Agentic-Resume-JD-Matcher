"""
graph/state.py

Defines the shared AgentState TypedDict that flows through
every node in the LangGraph pipeline.

"""
from __future__ import annotations
from typing import Optional, TypedDict

from backend.schemas.output import (
    ParsedResume,
    ParsedJD,
    SkillMatch,
    ATSScore,
    Recommendation,
    InterviewQuestions,
)


class AgentState(TypedDict, total=False):
    # ── Inputs ──────────────────────────────────────────────────────────────
    resume_text: str        # Raw text extracted from the uploaded PDF
    jd_text: str            # Raw job description text from the user

    # ── Agent outputs (populated sequentially by each node) ──────────────
    parsed_resume: Optional[ParsedResume]
    parsed_jd: Optional[ParsedJD]
    skill_match: Optional[SkillMatch]
    ats_score: Optional[ATSScore]
    recommendations: Optional[Recommendation]
    interview_questions: Optional[InterviewQuestions]

    # ── Control ──────────────────────────────────────────────────────────
    error: Optional[str]    # Set by any node that fails; checked by all downstream nodes
