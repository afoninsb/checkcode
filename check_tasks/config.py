import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DOMAIN: str = os.getenv('DOMAIN')
    REDIS_DSN: str = os.getenv('REDIS_DSN')
    RESULT_EXPIRES: int = 3600
    TEMPLATE_EMAIL: str = './check_tasks/template.txt'
    SMTP_HOST: str = os.getenv('SMTP_HOST')
    SMTP_PORT: int = os.getenv('SMTP_PORT')
    SMTP_EMAIL: str = os.getenv('SMTP_EMAIL')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: int = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    CHECK_INTERVAL: int = 1  # minutes
    EMAIL_INTERVAL: int = 2  # minutes
    REPORT_LINK: str = f'http://{DOMAIN}/reports'


config = Config()
