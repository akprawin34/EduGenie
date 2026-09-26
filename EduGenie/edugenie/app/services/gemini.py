import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.config import get_settings
from app.services.prompts import (
    EXPLAIN_PROMPT,
    LEARNING_PATH_PROMPT,
    QA_PROMPT,
    QUIZ_PROMPT,
    SUMMARY_PROMPT,
)


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not self.settings.gemini_api_key:
                raise RuntimeError("GEMINI_API_KEY is not configured. Set it in .env or enable DEMO_MODE=true.")
            self._client = genai.Client(api_key=self.settings.gemini_api_key)
        return self._client

    def _generate(self, prompt: str, *, temperature: float = 0.4, max_tokens: int = 900) -> str:
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    def qna(self, question: str) -> str:
        return self._generate(QA_PROMPT.format(question=question))

    def explain(self, topic: str) -> str:
        return self._generate(EXPLAIN_PROMPT.format(topic=topic))

    def summarize(self, text: str) -> str:
        return self._generate(SUMMARY_PROMPT.format(text=text), max_tokens=700)

    def learning_path(self, topic: str) -> str:
        return self._generate(LEARNING_PATH_PROMPT.format(topic=topic), max_tokens=1200)

    def quiz(self, text: str) -> list[dict[str, Any]]:
        raw = self._generate(QUIZ_PROMPT.format(text=text), temperature=0.2, max_tokens=1000)
        return self._parse_quiz(raw)

    @staticmethod
    def _parse_quiz(raw: str) -> list[dict[str, Any]]:
        cleaned = raw.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Gemini returned invalid quiz JSON: {exc}") from exc

        if not isinstance(data, list) or len(data) != 3:
            raise RuntimeError("Gemini quiz response must contain exactly 3 questions.")

        result: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict):
                raise RuntimeError("Each quiz question must be a JSON object.")
            question = str(item.get("question", "")).strip()
            options = item.get("options")
            answer = str(item.get("answer", "")).strip()
            if not question or not isinstance(options, list) or len(options) != 4:
                raise RuntimeError("Each quiz question must contain a question and exactly 4 options.")
            options = [str(x).strip() for x in options]
            if any(not x for x in options) or answer not in options:
                raise RuntimeError("Quiz answer must exactly match one of the four options.")
            result.append({"question": question, "options": options, "answer": answer})
        return result


class DemoService:
    def qna(self, question: str) -> str:
        return f"Demo answer: Your question was '{question}'. Add a Gemini API key to receive an AI-generated answer."

    def explain(self, topic: str) -> str:
        return f"Demo explanation: {topic} is being demonstrated in offline mode. Add a Gemini API key for a generated explanation with examples."

    def summarize(self, text: str) -> str:
        words = text.split()
        excerpt = " ".join(words[:45])
        return f"Demo summary: {excerpt}{'...' if len(words) > 45 else ''}"

    def learning_path(self, topic: str) -> str:
        return (f"Demo learning path for {topic}\n\n"
                "Beginner (1–2 weeks): terminology, core concepts, and simple exercises.\n"
                "Intermediate (2–3 weeks): applied problems, projects, and review.\n"
                "Advanced (3–4+ weeks): deeper theory, optimization, and a capstone project.")

    def quiz(self, text: str) -> list[dict[str, Any]]:
        return [
            {"question": "Which mode is EduGenie currently using?", "options": ["Demo mode", "Database mode", "Offline browser only", "No mode"], "answer": "Demo mode"},
            {"question": "How many options does each generated question require?", "options": ["2", "3", "4", "5"], "answer": "4"},
            {"question": "What should be configured for real Gemini answers?", "options": ["GEMINI_API_KEY", "PORT_ONLY", "CSS_KEY", "HTML_KEY"], "answer": "GEMINI_API_KEY"},
        ]


def get_ai_service():
    settings = get_settings()
    return DemoService() if settings.demo_mode else GeminiService()
