from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Setting(BaseSettings):
    app_title: str
    database_url: str
    secret: str
    first_superuser_email: EmailStr
    first_superuser_password: str
    rebbitmq_url: str
    queue_name: str

    class Config:
        env_file = '.env'


setting = Setting()
