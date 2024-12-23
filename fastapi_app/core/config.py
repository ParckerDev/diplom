from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url = "sqlite+aiosqlite:///./fa_rent_db.sqlite3"


settings = Settings()