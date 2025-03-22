import asyncio
import subprocess

from fastapi import FastAPI

from app.core.config import setting
from app.api.router import main_router
from app.core.init_db import create_first_superuser


app = FastAPI(title=setting.app_title)

app.include_router(main_router)

worker_process = None


@app.on_event('startup')
async def startup():
    await create_first_superuser()
    global worker_process
    worker_process = subprocess.Popen(["arq", "app.background_tasks.connection.worker"])


@app.on_event('shutdown')
async def shutdown():
    global worker_process
    if worker_process:
        worker_process.terminate()
        worker_process.wait(timeout=5)
