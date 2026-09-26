# EduGenie — Gemini Powered Learning Assistant

EduGenie is a complete FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project brief. It provides:

- Q&A with Gemini
- simple topic explanations
- paragraph summarization
- 3-question multiple-choice quiz generation
- structured learning recommendations
- a browser UI and REST API
- deterministic demo mode for local UI/API testing without an API key

The supplied document described FastAPI, a simple HTML/CSS frontend, and modules for Q&A, explanation, quiz generation, summarization, and learning recommendations. This implementation keeps that feature set while replacing obsolete Gemini usage with the current `google-genai` SDK and keeping the API key in environment configuration.

## Project structure

```text
edugenie/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── api.py
│   └── services/
│       ├── __init__.py
│       ├── gemini.py
│       └── prompts.py
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. VS Code setup

Install Python 3.10+ and VS Code. Open the **edugenie** folder in VS Code.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## 2. Configure Gemini

Create a Gemini API key in Google AI Studio, then put it in `.env`:

```env
GEMINI_API_KEY=YOUR_REAL_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
DEMO_MODE=false
```

Do not commit `.env` to Git. The source document included a key-looking value; it is intentionally **not** copied into this project. If that value was a real key, rotate/revoke it before using the project.

If you want to test the whole UI without an API key, set:

```env
DEMO_MODE=true
```

## 3. Run

```bash
python -m uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000 — web app
- http://127.0.0.1:8000/docs — Swagger API docs
- http://127.0.0.1:8000/health — health check

## 4. Test

With the virtual environment activated:

```bash
pytest -q
```

The tests use demo mode and do not call Gemini.

## 5. API examples

### Q&A

```http
GET /api/qna?question=Why%20is%20the%20sky%20blue%3F
```

### Explanation

```json
POST /api/explain
{"topic":"Photosynthesis"}
```

### Summary

```json
POST /api/summarize
{"text":"The Industrial Revolution changed production by moving work from many hand processes toward mechanized factories."}
```

### Quiz

```json
POST /api/quiz
{"text":"The Pythagorean theorem states that for a right triangle a²+b²=c²."}
```

### Learning recommendations

```json
POST /api/learning-path
{"topic":"SQL"}
```

## Notes

The application validates inputs, returns useful HTTP errors, limits overly large text requests, parses Gemini quiz JSON safely, and keeps Gemini-specific code isolated in `app/services/gemini.py`.
