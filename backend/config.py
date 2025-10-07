from pydantic_settings import BaseSettings
from pydantic import EmailStr
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email settings (Resend)
    resend_api_key: str = os.getenv("RESEND_API_KEY", "")
    contact_email_to: str = os.getenv("CONTACT_EMAIL_TO", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
