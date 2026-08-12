from celery import Celery
from config import settings

celery_app = Celery(
    "spiderforge",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["tasks.crawler", "tasks.scanner"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    worker_max_tasks_per_child=100,
)
