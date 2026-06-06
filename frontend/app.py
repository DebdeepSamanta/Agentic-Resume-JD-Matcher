"""
frontend/app.py

Streamlit is used

"""
import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RESUME ANALYZER",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.stApp { background: #0a0e1a; color: #e8eaf6; }

.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero h1 {
    font-size: 3rem; font-weight: 700; margin: 0; letter-spacing: -1px;
    background: linear-gradient(135deg, #6ee7f7 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: #94a3b8; font-size: 1.05rem; margin-top: 0.5rem; }

.metric-card {
    background: #131929; border: 1px solid #1e2d4a;
    border-radius: 16px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;
}
.metric-card .value {
    font-size: 2.8rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.metric-card .label {
    font-size: 0.8rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 1px; margin-top: 0.4rem;
}
.score-good { color: #4ade80; }
.score-mid  { color: #facc15; }
.score-low  { color: #f87171; }

.section-title {
    font-size: 1.05rem; font-weight: 600; color: #a78bfa;
    border-left: 3px solid #a78bfa; padding-left: 0.75rem;
    margin: 1.5rem 0 1rem; font-family: 'JetBrains Mono', monospace;
}

.pill-container { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.8rem; }
.pill { padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.78rem; font-weight: 600; }
.pill-green  { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.pill-red    { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }
.pill-blue   { background: #0c1a3a; color: #60a5fa; border: 1px solid #1e3a6a; }
.pill-purple { background: #1a0a3a; color: #c4b5fd; border: 1px solid #4c1d95; }

.info-box {
    background: #131929; border: 1px solid #1e2d4a; border-radius: 12px;
    padding: 1rem 1.25rem; margin-bottom: 0.75rem;
    font-size: 0.88rem; color: #cbd5e1; line-height: 1.6;
}
.info-box strong { color: #e2e8f0; }

.bar-wrap { margin-bottom: 0.6rem; }
.bar-label { display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.2rem; }
.bar-bg { background: #1e2d4a; border-radius: 999px; height: 8px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; }

.step-badge {
    display: inline-block; background: #1e2d4a; color: #60a5fa;
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700;
    padding: 0.15rem 0.5rem; border-radius: 6px; margin-right: 0.5rem;
}

div[data-testid="stFileUploader"] {
    background: #131929 !important; border: 2px dashed #2d4a7a !important;
    border-radius: 16px !important; padding: 1.5rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6ee7f7, #a78bfa) !important;
    color: #0a0e1a !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.75rem 2rem !important; font-size: 1rem !important;
    width: 100% !important; font-family: 'Sora', sans-serif !important;
}

textarea { background: #131929 !important; border: 1px solid #1e2d4a !important;
    border-radius: 12px !important; color: #e8eaf6 !important; }

button[data-baseweb="tab"] { background: transparent !important; color: #64748b !important; font-weight: 600 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #a78bfa !important; border-bottom: 2px solid #a78bfa !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def score_color(s: int) -> str:
    return "score-good" if s >= 75 else "score-mid" if s >= 50 else "score-low"


def pills(items: list, style: str):
    html = '<div class="pill-container">'
    for item in (items or ["—"]):
        html += f'<span class="pill pill-{style}">{item}</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def bar(label: str, score: int):
    color = "#4ade80" if score >= 75 else "#facc15" if score >= 50 else "#f87171"
    st.markdown(f"""
    <div class="bar-wrap">
      <div class="bar-label"><span>{label}</span><span>{score}/100</span></div>
      <div class="bar-bg"><div class="bar-fill" style="width:{score}%;background:{color};"></div></div>
    </div>""", unsafe_allow_html=True)


def info(text: str):
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def info_list(items: list):
    for item in (items or ["No data."]):
        info(f"• {item}")


def section(title: str, step: str = ""):
    badge = f'<span class="step-badge">{step}</span>' if step else ""
    st.markdown(f'<div class="section-title">{badge}{title}</div>', unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
  <h1>🎯 Resume Analyzer AI</h1>
  <p>Agentic Resume Analysis · ATS Scoring · Career Coaching · Interview Prep</p>
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────

col_l, col_r = st.columns(2, gap="large")

with col_l:
    section("Upload Resume", "01")
    uploaded = st.file_uploader("Resume PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded:
        st.success(f"✓ {uploaded.name}  ({uploaded.size // 1024} KB)")

with col_r:
    section("Paste Job Description", "02")
    jd_text = st.text_area("Job Description", placeholder="Paste the full job description here...",
                            height=180, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run = st.button("⚡ Analyse My Resume", use_container_width=True)

st.markdown("---")

# ── Run pipeline ──────────────────────────────────────────────────────────────

if run:
    if not uploaded:
        st.error("Please upload a resume PDF.")
        st.stop()
    if not jd_text.strip():
        st.error("Please paste a job description.")
        st.stop()

    agent_steps = [
        "📄 Agent 1 — Parsing resume...",
        "🔍 Agent 2 — Analysing job description...",
        "🔗 Agent 3 — Matching skills...",
        "📊 Agent 4 — Computing ATS score...",
        "💡 Agent 5 — Generating recommendations...",
        "🎤 Agent 6 — Creating interview questions...",
    ]

    with st.status("🤖 Running AI Agent Pipeline...", expanded=True) as status:
        phs = [st.empty() for _ in agent_steps]
        for ph, step in zip(phs, agent_steps):
            ph.markdown(step)

        try:
            resp = requests.post(
                f"{API_URL}/analyze",
                files={"resume": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                data={"job_description": jd_text},
                timeout=300,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.exceptions.ConnectionError:
            status.update(label="❌ Cannot reach backend", state="error")
            st.error(f"Could not connect to `{API_URL}`. Is the FastAPI server running?")
            st.stop()
        except Exception as e:
            status.update(label="❌ Request failed", state="error")
            st.error(str(e))
            st.stop()

        if not result.get("success"):
            status.update(label="❌ Pipeline error", state="error")
            st.error(result.get("error", "Unknown error from pipeline."))
            st.stop()

        for ph, step in zip(phs, agent_steps):
            ph.markdown(f"✅ {step}")

        status.update(label="✅ Analysis complete!", state="complete")

    # ── Unpack report ─────────────────────────────────────────────────────
    rpt = result["report"]
    cv  = rpt["parsed_resume"]
    jd  = rpt["parsed_jd"]
    sm  = rpt["skill_match"]
    ats = rpt["ats_score"]
    rec = rpt["recommendations"]
    iq  = rpt["interview_questions"]

    # ── Score cards ───────────────────────────────────────────────────────
    required_skills = len(jd.get("required_skills", []))
    matched_skills = len(sm.get("matched_skills", []))
    missing_skills = len(sm.get("missing_skills", []))

    skill_coverage = round(
        (matched_skills / max(required_skills, 1)) * 100
    )

    st.markdown("## 📊 Results Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (c1, ats["overall_score"], "ATS Score"),
        (c2, skill_coverage, "Skill Coverage"),
        (c3, ats["experience_score"], "Experience Match"),
        (c4, missing_skills, "Missing Skills"),
    ]

    for col, val, label in metrics:
        with col:

            if label == "Missing Skills":
                cls = "score-low"
            else:
                cls = score_color(val)

            st.markdown(f"""
            <div class="metric-card">
                <div class="value {cls}">{val}</div>
                <div class="label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    # ── Tabs ──────────────────────────────────────────────────────────────
    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📋 Resume Profile",
        "🎯 Skill Match",
        "📈 ATS Breakdown",
        "💡 Recommendations",
        "🎤 Interview Prep",
        "📄 Raw JSON",
    ])

    # Tab 1 — Resume Profile
    with t1:
        a, b = st.columns(2, gap="large")
        with a:
            section("Candidate Info")
            for k, v in [("Name", cv.get("name")), ("Email", cv.get("email")),
                          ("Phone", cv.get("phone")), ("Location", cv.get("location"))]:
                info(f"<strong>{k}:</strong> {v or '—'}")
            section("Professional Summary")
            info(cv.get("summary") or "No summary found.")
        with b:
            section("Target Role")
            info(f"<strong>{jd.get('job_title', '—')}</strong> at {jd.get('company') or 'not specified'}")
            section("Skills")
            pills(cv.get("skills", []), "purple")
            section("Certifications")
            pills(cv.get("certifications") or ["None listed"], "blue")

        section("Work Experience")
        for exp in cv.get("experience", []):
            with st.expander(f"🏢 {exp.get('title')} @ {exp.get('company')} — {exp.get('duration')}"):
                st.write(exp.get("description") or "No description.")

        section("Education")
        for edu in cv.get("education", []):
            info(f"🎓 <strong>{edu.get('degree')}</strong> — {edu.get('institution')} ({edu.get('year', '')})")

    # Tab 2 — Skill Match
    with t2:
        c1, c2, c3 = st.columns(3)
        with c1:
            section("✅ Matched Skills")
            pills(sm.get("matched_skills", []), "green")
        with c2:
            section("❌ Missing Skills")
            pills(sm.get("missing_skills", []), "red")
        with c3:
            section("⭐ Bonus Skills")
            pills(sm.get("bonus_skills", []), "blue")

        section("JD Required Skills")
        pills(jd.get("required_skills", []), "purple")
        section("JD Preferred Skills")
        pills(jd.get("preferred_skills", []), "blue")
        section("ATS Keywords in JD")
        pills(jd.get("keywords", []), "green")

    # Tab 3 — ATS Breakdown
    with t3:
        a, b = st.columns(2, gap="large")
        with a:
            section("Score Breakdown")
            for label, key in [
                ("Overall ATS Score",    "overall_score"),
                ("Keyword Density",      "keyword_score"),
                ("Format & Structure",   "format_score"),
                ("Experience Alignment", "experience_score"),
                ("Education Match",      "education_score"),
            ]:
                bar(label, ats[key])
        with b:
            section("Section Comments")
            for k, v in ats.get("breakdown", {}).items():
                info(f"<strong>{k.capitalize()}:</strong> {v}")

    # Tab 4 — Recommendations
    with t4:
        for title, key in [
            ("✍️ Improve Your Summary",     "summary_suggestions"),
            ("📚 Skills to Learn / Add",    "skills_to_add"),
            ("⚠️ Experience Gaps",          "experience_gaps"),
            ("⚡ Quick Wins (Do Today)",    "quick_wins"),
            ("🚀 Long-Term Actions",        "long_term_actions"),
        ]:
            section(title)
            info_list(rec.get(key, []))

    # Tab 5 — Interview Prep
    with t5:
        for title, key in [
            ("🔧 Technical Questions",    "technical"),
            ("🤝 Behavioral Questions",   "behavioral"),
            ("🎯 Role-Specific Questions","role_specific"),
        ]:
            section(title)
            for i, q in enumerate(iq.get(key, []), 1):
                info(f"<strong>Q{i}.</strong> {q}")

        section("💬 Answer Tips")
        info_list(iq.get("suggested_answers_tips", []))

    # Tab 6 — Raw JSON
    with t6:
        section("Full Report JSON")
        st.json(rpt)

else:
    # Landing state
    st.markdown("""
    <div style="text-align:center;padding:3rem 0;color:#475569;">
      <div style="font-size:4rem;margin-bottom:1rem;">🤖</div>
      <p style="font-size:1.05rem;">
        Upload your resume PDF and paste a job description above,<br>
        then click <strong style="color:#a78bfa">Analyse My Resume</strong> to start the pipeline.
      </p>
      <br>
      <div style="display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap;color:#64748b;font-size:0.85rem;">
        <span>📄 Resume Parser</span><span>→</span>
        <span>🔍 JD Analyser</span><span>→</span>
        <span>🔗 Skill Matcher</span><span>→</span>
        <span>📊 ATS Scorer</span><span>→</span>
        <span>💡 Recommender</span><span>→</span>
        <span>🎤 Interview Coach</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
