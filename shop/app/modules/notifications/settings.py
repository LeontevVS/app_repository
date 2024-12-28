from pydantic_settings import BaseSettings

from config import EmailSenderConfig


class Settings(BaseSettings):
    email_sender: EmailSenderConfig = EmailSenderConfig()


SETTINGS = Settings()
