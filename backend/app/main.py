from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import model
from .api.log_api import router as log_router
from .api.service_api import router as service_router
from .api.statistics_api import router as statistics_router
from .config import get_settings
from .database import Base, engine
from .seed import seed_demo_data
from .task.statistics_task import calculate_yesterday_statistics
from .task.status_task import refresh_all_statuses

settings = get_settings()
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    if settings.enable_demo_data:
        seed_demo_data()
    scheduler.add_job(
        refresh_all_statuses,
        "interval",
        seconds=settings.status_scan_seconds,
        id="status-scan",
        replace_existing=True,
    )
    scheduler.add_job(
        calculate_yesterday_statistics,
        "cron",
        hour=0,
        minute=10,
        id="daily-statistics",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(log_router, prefix="/api")
app.include_router(service_router, prefix="/api")
app.include_router(statistics_router, prefix="/api")


@app.get("/api/health", tags=["系统"])
def health():
    return {"status": "ok"}
