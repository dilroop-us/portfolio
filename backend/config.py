from pydantic_settings import BaseSettings
from pydantic import EmailStr
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    mail_username: str = os.getenv("MAIL_USERNAME", "")
    mail_password: str = os.getenv("MAIL_PASSWORD", "")
    mail_from: EmailStr = os.getenv("MAIL_FROM", "noreply@example.com")
    mail_from_name: str = os.getenv("MAIL_FROM_NAME", "Portfolio Contact Form")
    mail_to: EmailStr = os.getenv("MAIL_TO", "your-email@example.com")
    mail_port: int = int(os.getenv("MAIL_PORT", "587"))
    mail_server: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_starttls: bool = os.getenv("MAIL_STARTTLS", "true").lower() == "true"
    mail_ssl_tls: bool = os.getenv("MAIL_SSL_TLS", "false").lower() == "true"
    mail_use_credentials: bool = os.getenv("MAIL_USE_CREDENTIALS", "true").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()
