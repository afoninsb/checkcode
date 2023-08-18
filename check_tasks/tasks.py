import logging
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import redis
from celery import Celery
from celery.schedules import crontab
from celery.signals import after_setup_logger
from config import config
from db import save_result, update_result
from functions import read_template

logger = logging.getLogger(__name__)

r = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True
)

app = Celery(
    'tasks',
    broker=f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}',
    backend=f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}',
)

app.conf.update(
    result_expires=config.RESULT_EXPIRES,
)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Расписание периодических задач."""
    sender.add_periodic_task(
        crontab(minute=f'*/{config.CHECK_INTERVAL}'),
        check_code.s(),
    )
    sender.add_periodic_task(
        crontab(minute=f'*/{config.EMAIL_INTERVAL}'),
        send_email.s(),
    )


@app.task
def check_code():
    """Запускаем проверку файлов в очереди и отправляем на отправку."""
    length = r.llen('to_check')
    if length == 0:
        return
    codes = r.lpop('to_check', length)
    for code in codes:
        code_id, code_path, code_name, user_email = code.split(':')
        # Посылаем на анализ - запускаем функцию или POST-запрос на API

        # Моделируем результат проверки
        result = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...'
        status = 'accepted' if random.random() < 0.5 else 'rejected'
        check_id = save_result({
            'code_id': code_id,
            'result': result,
            'status': status,
            'sent_email': False
        })
        r.lpush(
            'to_email',
            f'{check_id}:{user_email}:{code_id}:{code_name}:{status}'
        )


@app.task
def send_email():
    """Отправляем по почте результаты анализа."""
    length = r.llen('to_email')
    if length == 0:
        return
    codes = r.lpop('to_email', length)
    for code in codes:
        check_id, email, code_id, code_name, code_status = code.split(':')
        message_template = read_template()
        s = smtplib.SMTP(host=config.SMTP_HOST, port=config.SMTP_PORT)
        s.starttls()
        a = s.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
        msg = MIMEMultipart()
        message = message_template.substitute(
            NAME=code_name,
            STATUS=code_status,
            LINK=f'{config.REPORT_LINK}/{code_id}/'
        )
        msg['From'] = config.SMTP_EMAIL
        msg['To'] = email
        msg['Subject'] = 'Ваш файл проверен'
        msg.attach(MIMEText(message, 'html'))  # plain
        s.send_message(msg)
        s.quit()
        update_result(check_id)


if __name__ == '__main__':
    app.start()
