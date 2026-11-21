# ResumeIQ 🧠📄
### AI-Powered Resume Evaluator & Career Intelligence System

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FHemantSharma456%2FAIResume-Evaluator-v2)
![GitHub Repo](https://img.shields.io/badge/GitHub-HemantSharma456%2FAIResume--Evaluator--v2-blue?style=flat-square&logo=github)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Serverless-black?style=flat-square&logo=flask)
![Vercel](https://img.shields.io/badge/Vercel-Deploy%20Ready-black?style=flat-square&logo=vercel)
![Milestone](https://img.shields.io/badge/Prompt%20Engineering-Milestone%202%20Submission-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> Upload your resume, paste an optional Job Description, and get instant, structured career intelligence: statistical ATS rubric scores, recruiter alignment diagnosis, Google XYZ bullet transformations with 1-click copy, verified vs. missing skill gaps, section-by-section advice, and a 3-phase career roadmap.

---

## 🌟 Highlights & Architecture

ResumeIQ combines **two complementary intelligence layers** without sacrificing statistical rigor:

1. **Statistical ML Model Layer (`ml_model.py`)**:
   - Pre-trained TF-IDF vectorizer + Logistic Regression classifier on 2,400+ categorized resumes.
   - 100-point deterministic ATS rubric across 8 weighted sections.
   - Guaranteed consistency and zero hallucinations for numerical scoring.

2. **Modular Prompt Engineering Engine (`ai_engine/`)**:
   - Modular prompt architecture with separate contracts for Contextual Analysis, Competency Gap Audit, Bullet Transformations, and Career Feedback.
   - Built-in multi-provider resilience: supports Google Gemini (`gemini-1.5-flash`), OpenAI (`gpt-4o-mini`), and local offline deterministic fallback.
   - Comprehensive prompt versioning (V1 Baseline → V2 Structured → V3 JSON Schema → Final Production).
   - Automated experimentation runner (`ai_engine/experimentation/`) with 16 logged experiments.
   - 10-case automated test suite (`tests/test_ai_suite.py`) with 100% pass verification.

---

## 🎛️ 5 Interactive Dashboard Modules

The user interface features an **Option Matrix Dashboard** with a **Dual View Controller** (`🎛️ Single Option View` vs. `📑 Show All Options`):

| Module | Description | Core Capabilities |
| :--- | :--- | :--- |
| **Option 1: Recruiter Match (`🎯`)** | Executive Recruiter Diagnosis & Alignment | Role alignment score, seniority fit analysis, verified candidate strengths, and critical friction points. |
| **Option 2: Bullet Studio (`⚡`)** | Google XYZ Bullet Transformations | Weakness diagnosis, power verb elevation, Google XYZ formula (`Accomplished [X] by doing [Z] as measured by [Y]`), and **1-Click Copy Buttons (`📋 Copy`)**. |
| **Option 3: Skill Gap Audit (`🔍`)** | Competency Breakdown & Filter | Interactive filterable tags across Verified Demonstrated, Critical Missing, Partially Demonstrated, and Transferable Bridges. |
| **Option 4: Section Advice (`📝`)** | Section-by-Section ATS Gains | Action items with rubric point gains across Summary, Experience, Projects, Skills, and ATS Formatting. |
| **Option 5: Career Roadmap (`🚀`)** | 3-Phase Action Plan | Actionable 7-day, 30-day, and 90-day trajectory with curated skills and portfolio project concepts. |

---

## 🚀 Live Vercel Deployment

Deploy directly to Vercel in 1 click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FHemantSharma456%2FAIResume-Evaluator-v2)

### Deploying via Vercel Dashboard
1. Go to [vercel.com/new](https://vercel.com/new).
2. Select **Import Git Repository** and choose **`HemantSharma456/AIResume-Evaluator-v2`**.
3. (Optional) In **Environment Variables**, add:
   - `GEMINI_API_KEY` (or `OPENAI_API_KEY`) for live cloud LLM integration.
   - If omitted, the engine automatically uses its built-in offline deterministic AI mode with zero external dependencies!
4. Click **Deploy**. Vercel will build and assign your production URL (e.g. `https://airesume-evaluator-v2.vercel.app`).

### Deploying via Vercel CLI
```bash
# 1. Install or run Vercel CLI
npx vercel login

# 2. Deploy to production
npx vercel --prod
```

---

## 💻 Local Quickstart

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/HemantSharma456/AIResume-Evaluator-v2.git
cd AIResume-Evaluator-v2
```

### 2. Set up virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment (Optional)
```bash
cp .env.example .env
# Edit .env with your GEMINI_API_KEY or OPENAI_API_KEY if desired
```

### 5. Launch the application
```bash
python app.py
```
Open [http://127.0.0.1:4000](http://127.0.0.1:4000) in your browser.

---

## 🧪 Testing & Evaluation Suite

Run the 10-case systematic test suite:
```bash
python tests/test_ai_suite.py
```

Run the automated prompt experimentation suite:
```bash
python ai_engine/experimentation/experiment_runner.py
```

---

## 📄 Documentation

- [Prompt Engineering Milestone 2 Report](PROMPT_ENGINEERING_MILESTONE_2.md) — Comprehensive technical report detailing prompt iteration logs, anti-hallucination guardrails, and evaluation matrices.

## 📜 License
Distributed under the MIT License.
