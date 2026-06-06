"""
graph/workflow.py

Builds and compiles the LangGraph multi-agent pipeline.

Node order:
  parse_resume → analyze_jd → match_skills → score_ats
  → recommend → generate_interview_questions → END

"""
from langgraph.graph import StateGraph, END

from backend.graph.state import AgentState
from backend.agents.resume_parser import run_resume_parser
from backend.agents.jd_analyzer import run_jd_analyzer
from backend.agents.skill_matcher import run_skill_matcher
from backend.agents.ats_scorer import run_ats_scorer
from backend.agents.recommender import run_recommender
from backend.agents.interview_generator import run_interview_generator
from backend.schemas.output import FinalReport


# ── Node definitions ──────────────────────────────────────────────────────────

def node_parse_resume(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["parsed_resume"] = run_resume_parser(state["resume_text"])
    except Exception as exc:
        state["error"] = f"[Resume Parser] {exc}"
    return state


def node_analyze_jd(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["parsed_jd"] = run_jd_analyzer(state["jd_text"])
    except Exception as exc:
        state["error"] = f"[JD Analyser] {exc}"
    return state


def node_match_skills(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["skill_match"] = run_skill_matcher(
            state["parsed_resume"],
            state["parsed_jd"],
        )
    except Exception as exc:
        state["error"] = f"[Skill Matcher] {exc}"
    return state


def node_score_ats(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["ats_score"] = run_ats_scorer(
            state["parsed_resume"],
            state["parsed_jd"],
            state["skill_match"],
        )
    except Exception as exc:
        state["error"] = f"[ATS Scorer] {exc}"
    return state


def node_recommend(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["recommendations"] = run_recommender(
            state["parsed_resume"],
            state["parsed_jd"],
            state["skill_match"],
            state["ats_score"],
        )
    except Exception as exc:
        state["error"] = f"[Recommender] {exc}"
    return state


def node_generate_interview_questions(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        state["interview_questions"] = run_interview_generator(
            state["parsed_resume"],
            state["parsed_jd"],
        )
    except Exception as exc:
        state["error"] = f"[Interview Generator] {exc}"
    return state


# ── Graph builder ─────────────────────────────────────────────────────────────

def build_workflow():
    """Construct and compile the LangGraph StateGraph."""
    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node("parse_resume",               node_parse_resume)
    graph.add_node("analyze_jd",                 node_analyze_jd)
    graph.add_node("match_skills",               node_match_skills)
    graph.add_node("score_ats",                  node_score_ats)
    graph.add_node("recommend",                  node_recommend)
    graph.add_node("generate_interview_questions", node_generate_interview_questions)

    # Entry point
    graph.set_entry_point("parse_resume")

    # Sequential edges
    graph.add_edge("parse_resume",               "analyze_jd")
    graph.add_edge("analyze_jd",                 "match_skills")
    graph.add_edge("match_skills",               "score_ats")
    graph.add_edge("score_ats",                  "recommend")
    graph.add_edge("recommend",                  "generate_interview_questions")
    graph.add_edge("generate_interview_questions", END)

    return graph.compile()


# ── Public runner ─────────────────────────────────────────────────────────────

def run_workflow(resume_text: str, jd_text: str) -> FinalReport:
    """
    Execute the full agent pipeline and return a FinalReport.

    Args:
        resume_text: Plain text extracted from the candidate's resume PDF.
        jd_text: Raw job description text.

    Returns:
        FinalReport: Fully populated report from all 6 agents.

    Raises:
        RuntimeError: If any agent fails during execution.
    """
    pipeline = build_workflow()

    initial_state: AgentState = {
        "resume_text": resume_text,
        "jd_text": jd_text,
        "parsed_resume": None,
        "parsed_jd": None,
        "skill_match": None,
        "ats_score": None,
        "recommendations": None,
        "interview_questions": None,
        "error": None,
    }

    final_state = pipeline.invoke(initial_state)

    if final_state.get("error"):
        raise RuntimeError(final_state["error"])

    return FinalReport(
        parsed_resume=final_state["parsed_resume"],
        parsed_jd=final_state["parsed_jd"],
        skill_match=final_state["skill_match"],
        ats_score=final_state["ats_score"],
        recommendations=final_state["recommendations"],
        interview_questions=final_state["interview_questions"],
    )
