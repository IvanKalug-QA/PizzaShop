from fastapi import FastAPI

from app.core.config import setting
from app.api.router import main_router
from app.core.init_db import create_first_superuser


app = FastAPI(title=setting.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
