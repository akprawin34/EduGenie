from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = "EduGenie"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    demo_mode: bool = os.getenv("DEMO_MODE", "false").strip().lower() in {"1", "true", "yes", "on"}
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    max_input_chars: int = 12000


@lru_cache
def get_settings() -> Settings:
    return Settings()
