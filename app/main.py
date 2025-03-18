from fastapi import FastAPI

from app.core.config import setting


app = FastAPI(title=setting.app_title)
