# 🎯 Resume Analyzer AI — Agentic Resume–JD Matcher

An end-to-end AI agent pipeline that parses your resume, analyses the job description,
scores ATS compatibility provides recommendations and tailored interview questions.

---

## Project Structure

```
resume-jd-matcher/
│
├── frontend/
│   └── app.py                      # Streamlit UI
│
├── backend/
│   ├── main.py                     # FastAPI app + endpoints
│   │
│   ├── graph/
│   │   ├── state.py                # LangGraph AgentState TypedDict
│   │   └── workflow.py             # LangGraph pipeline (nodes + edges)
│   │
│   ├── agents/
│   │   ├── resume_parser.py        # Agent 1 — parse resume
│   │   ├── jd_analyzer.py          # Agent 2 — analyse JD
│   │   ├── skill_matcher.py        # Agent 3 — match skills
│   │   ├── ats_scorer.py           # Agent 4 — ATS score
│   │   ├── recommender.py          # Agent 5 — recommendations
│   │   └── interview_generator.py  # Agent 6 — interview questions
│   │
│   ├── services/
│   │   ├── llm.py                  # Groq LLM client (call_llm, call_llm_json)
│   │   └── pdf_parser.py           # PyMuPDF text extraction
│   │
│   └── schemas/
│       └── output.py               # All Pydantic v2 models
│
├── uploads/                        # Uploaded PDFs saved here
├── .env                            # API keys (never commit)
├── requirements.txt
├── Dockerfile
├── docker-entrypoint.sh
└── README.md
```

---

## Tech Stack

| Layer         | Technology                     |
|---------------|-------------------------------|
| Frontend      | Streamlit                      |
| Backend API   | FastAPI + Uvicorn              |
| Orchestration | LangGraph                      |
| LLM           | Groq — Llama 3.3 70B           |
| PDF Parsing   | PyMuPDF (fitz)                 |
| Validation    | Pydantic v2                    |
| Deployment    | Docker                         |

---


## API Reference

| Method | Path            | Description                           |
|--------|-----------------|---------------------------------------|
| GET    | `/health`       | Liveness check + model name           |
| POST   | `/analyze`      | PDF upload + JD text → FinalReport    |
| POST   | `/analyze-text` | Raw text resume + JD → FinalReport    |
| GET    | `/docs`         | Swagger UI (auto-generated)           |

---

## Agent Pipeline

```
Upload PDF + JD Text
        │
        ▼
  FastAPI /analyze
        │
        ▼
  LangGraph Workflow
  ┌──────────────────────────────────────────────────────┐
  │  Node 1: parse_resume        → ParsedResume          │
  │  Node 2: analyze_jd          → ParsedJD              │
  │  Node 3: match_skills        → SkillMatch            │
  │  Node 4: score_ats           → ATSScore              │
  │  Node 5: recommend           → Recommendation        │
  │  Node 6: generate_interview  → InterviewQuestions    │
  └──────────────────────────────────────────────────────┘
        │
        ▼
   FinalReport (Pydantic)
        │
        ▼
  Streamlit Dashboard
```

Each node short-circuits on error — downstream agents are skipped safely.

---

