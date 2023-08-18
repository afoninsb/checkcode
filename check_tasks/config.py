import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DOMAIN: str = os.getenv('DOMAIN')
    REDIS_DSN: str = os.getenv('REDIS_DSN')
    RESULT_EXPIRES: int = 3600
    TEMPLATE_EMAIL: str = 'template.txt'
    SMTP_HOST: str = os.getenv('SMTP_HOST')
    SMTP_PORT: int = os.getenv('SMTP_PORT')
    SMTP_EMAIL: os.getenv('SMTP_EMAIL')
    SMTP_PASSWORD: os.getenv('SMTP_PASSWORD')
    DB_NAME = os.getenv('DB_NAME', default='postgres'),
    DB_USER = os.getenv('DB_USER', default='postgres'),
    DB_PASSWORD = os.getenv('DB_PASSWORD', default='postgres'),
    DB_HOST = os.getenv('DB_HOST', default='localhost'),
    DB_PORT = os.getenv('DB_PORT', default='5432')
    DB_URI = (
        f'postgresql://{DB_USER}:{DB_PASSWORD}'
        f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )


config = Config()
