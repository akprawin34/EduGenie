from fastapi import APIRouter, HTTPException, Query

from app.schemas import (
    ExplanationResponse,
    LearningPathResponse,
    QuestionResponse,
    QuizResponse,
    SummaryResponse,
    TextRequest,
    TopicRequest,
)
from app.services.gemini import get_ai_service

router = APIRouter(prefix="/api", tags=["EduGenie"])


def run_ai(callable_, *args):
    try:
        return callable_(*args)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI service error: {exc}") from exc


@router.get("/qna", response_model=QuestionResponse)
async def qna(question: str = Query(..., min_length=2, max_length=1000)):
    return {"answer": run_ai(get_ai_service().qna, question.strip())}


@router.post("/explain", response_model=ExplanationResponse)
async def explain(request: TopicRequest):
    return {"topic": request.topic, "explanation": run_ai(get_ai_service().explain, request.topic)}


@router.post("/summarize", response_model=SummaryResponse)
async def summarize(request: TextRequest):
    return {"summary": run_ai(get_ai_service().summarize, request.text)}


@router.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    return {"quiz": run_ai(get_ai_service().quiz, request.text)}


@router.post("/learning-path", response_model=LearningPathResponse)
async def learning_path(request: TopicRequest):
    return {"topic": request.topic, "recommendations": run_ai(get_ai_service().learning_path, request.topic)}
