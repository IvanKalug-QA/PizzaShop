from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    app_title: str
    database_url: str

    class Config:
        env_file = '.env'


setting = Setting()
