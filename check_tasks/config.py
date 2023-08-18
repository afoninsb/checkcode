import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DOMAIN: str = os.getenv('DOMAIN')
    REDIS_DSN: str = os.getenv('REDIS_DSN')
    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: str = os.getenv('REDIS_PORT')
    RESULT_EXPIRES: int = 3600
    TEMPLATE_EMAIL: str = 'template.txt'
    SMTP_HOST: str = os.getenv('SMTP_HOST')
    SMTP_PORT: int = os.getenv('SMTP_PORT')
    SMTP_EMAIL: str = os.getenv('SMTP_EMAIL')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
    DB_NAME: str = os.getenv('POSTGRES_DB')
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DB_HOST: int = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    CHECK_INTERVAL: int = 1  # minutes
    EMAIL_INTERVAL: int = 2  # minutes
    REPORT_LINK: str = f'http://{DOMAIN}/reports'


config = Config()
