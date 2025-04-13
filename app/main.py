import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_redis_cache import FastApiRedisCache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import setting
from app.api.router import main_router
from app.logs.config import setup_loggers

setup_loggers()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=setting.app_title)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[setting.main_host,],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

worker_process = None


@app.on_event('startup')
async def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(host_url=setting.cache_redis_url)
    global worker_process
    worker_process = subprocess.Popen(
        ["arq", "app.background_tasks.connection.worker"])


@app.on_event('shutdown')
async def shutdown():
    global worker_process
    if worker_process:
        worker_process.terminate()
        worker_process.wait(timeout=5)
