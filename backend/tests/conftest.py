import os
from pathlib import Path


TEST_DATABASE = Path(__file__).resolve().parent.parent / "test_log_assistant.db"

os.environ["DATABASE_URL"] = "sqlite:///./test_log_assistant.db"
os.environ["ALLOWED_LOG_ROOT"] = "./runtime_logs"
os.environ["ENABLE_DEMO_DATA"] = "true"


def pytest_sessionfinish():
    from app.database import engine

    engine.dispose()
    TEST_DATABASE.unlink(missing_ok=True)
