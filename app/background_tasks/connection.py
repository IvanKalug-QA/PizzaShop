from arq.worker import Worker
from arq.connections import RedisSettings
from arq.cron import cron

from app.core.config import setting
from app.background_tasks.tasks import check_rabbitmq


redis_settings = RedisSettings(host=setting.redis_host, port=6379)

worker = Worker(
    redis_settings=redis_settings,
    functions=["app.background_tasks.tasks.check_rabbitmq"],
    cron_jobs=[
        cron(
            name="app.background_tasks.tasks.check_rabbitmq",
            coroutine=check_rabbitmq, second=50)
    ],
)
