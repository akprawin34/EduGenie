from pydantic import BaseModel, Field, field_validator

MAX_TEXT = 12000


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=300)

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("Topic cannot be empty.")
        return value


class QuestionResponse(BaseModel):
    answer: str


class SummaryResponse(BaseModel):
    summary: str


class ExplanationResponse(BaseModel):
    topic: str
    explanation: str


class LearningPathResponse(BaseModel):
    topic: str
    recommendations: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str


class QuizResponse(BaseModel):
    quiz: list[QuizQuestion]
