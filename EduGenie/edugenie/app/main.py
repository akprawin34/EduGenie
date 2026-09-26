from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.routers.api import router as api_router

BASE_DIR = Path(__file__).resolve().parent.parent

settings = get_settings()
app = FastAPI(
    title="EduGenie API",
    description="Gemini-powered educational learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"demo_mode": settings.demo_mode})


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie",
        "demo_mode": settings.demo_mode,
        "gemini_configured": bool(settings.gemini_api_key),
    }
