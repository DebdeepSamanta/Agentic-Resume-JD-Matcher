# Resume Analyzer AI

A practical AI application that helps job seekers understand how well their resume matches a specific job description.

The application analyzes a resume against a job posting, identifies matching and missing skills, calculates an ATS-style compatibility score, and generates personalized recommendations and interview questions.

The project was built to explore agentic workflows using LangGraph while solving a real-world problem faced by candidates during the job application process.

## Features

* Upload a resume in PDF format
* Analyze any job description
* Extract skills, experience, certifications, and projects from resumes
* Identify matched and missing skills
* Generate an ATS-style compatibility score
* Provide actionable resume improvement suggestions
* Create a personalized learning roadmap
* Generate interview questions tailored to the candidate profile and target role

## Tech Stack

**Frontend**

* Streamlit

**Backend**

* FastAPI
* LangGraph

**LLM**

* Groq (Llama 3.3 70B)

**Supporting Libraries**

* LangChain
* PyMuPDF
* Pydantic
* Docker

## How It Works

The user uploads a resume and provides a job description.

The system processes both inputs through a multi-step workflow:

1. Resume Parsing

   * Extracts structured information from the resume.

2. Job Description Analysis

   * Identifies required skills, preferred skills, and role expectations.

3. Skill Matching

   * Compares candidate skills against job requirements.

4. ATS Scoring

   * Calculates a compatibility score based on the match.

5. Recommendations

   * Suggests improvements and highlights skill gaps.

6. Interview Preparation

   * Generates role-specific interview questions.

The final output is presented through an interactive Streamlit dashboard.

## Running Locally

Clone the repository:

```bash
git clone <repository-url>
cd resume-jd-matcher
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Start the frontend:

```bash
streamlit run frontend/app.py
```

## API Endpoints

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | /health       | Health check                  |
| POST   | /analyze      | Resume PDF + Job Description  |
| POST   | /analyze-text | Resume Text + Job Description |
| GET    | /docs         | Swagger Documentation         |

## Future Improvements

* Resume rewriting and optimization
* Multiple job description comparison
* Historical analysis tracking
* Authentication and user profiles
* Support for additional resume formats
* Deployment on cloud infrastructure

## ScreenShot

<img width="1888" height="916" alt="image" src="https://github.com/user-attachments/assets/aac7ad55-9a96-4b78-af8f-5c54d0d7766e" />

<img width="1854" height="885" alt="image" src="https://github.com/user-attachments/assets/64d5e399-5890-43ee-9fc0-a932f3867bf4" />

<img width="1851" height="620" alt="image" src="https://github.com/user-attachments/assets/a97ff05e-9d0f-441c-87e5-8a593bde60ea" />

<img width="1902" height="934" alt="image" src="https://github.com/user-attachments/assets/5bb8ab47-a0cf-479a-9acc-06954b117b47" />

<img width="1853" height="821" alt="image" src="https://github.com/user-attachments/assets/e25149fa-2ec6-4961-a5a2-595e4789a11b" />


## Motivation

As someone interested in Generative AI and Agentic AI systems, I wanted to build a project that goes beyond a typical chatbot and demonstrates how multiple AI-driven components can work together to solve a practical problem. This project combines document understanding, structured information extraction, workflow orchestration, and personalized recommendations into a single application.
