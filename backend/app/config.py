from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI 日志管理助手"
    database_url: str = "sqlite:///./log_assistant.db"  # 本地开发默认使用 SQLite
    allowed_log_root: str = "./runtime_logs"  # 本地开发允许读取的日志根目录
    enable_demo_data: bool = True  # 本地开发时生成示例数据
    status_scan_seconds: int = 60
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
