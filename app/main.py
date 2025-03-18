from fastapi import FastAPI

from app.core.config import setting
from app.api.router import main_router


app = FastAPI(title=setting.app_title)

app.include_router(main_router)
