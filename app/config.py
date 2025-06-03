import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configurations."""
    
    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY không được cấu hình. "
                "Vui lòng thêm OPENAI_API_KEY vào file .env"
            )

# Create settings instance
settings = Settings() 