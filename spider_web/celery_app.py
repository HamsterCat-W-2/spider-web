from celery import Celery
from spider_web.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

app = Celery(
    "spider_web",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Shanghai",
)

app.autodiscover_tasks(["spider_web"])
