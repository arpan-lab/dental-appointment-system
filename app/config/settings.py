from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Groq
    groq_api_key: str

    # LLM configuration
    model_name: str = "openai/gpt-oss-20b"
    temperature: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()