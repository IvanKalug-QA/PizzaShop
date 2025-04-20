from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Setting(BaseSettings):
    app_title: str
    database_url: str
    secret: str
    first_superuser_email: EmailStr
    first_superuser_password: str
    rabbitmq_url: str
    queue_name: str
    mail_server: str
    mail_username: str
    mail_password: str
    redis_host: str
    main_host: str
    cache_redis_url: str

    class Config:
        env_file = '.env'


setting = Setting()
