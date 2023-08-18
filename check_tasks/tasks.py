import os
from check_code.files.models import CheckStatus
from check_tasks.db import save_result, update_result
from check_tasks.celery import app
import redis
import random
import smtplib

from check_tasks.functions import read_template
from check_tasks.config import config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

r = redis.Redis(decode_responses=True)


@app.task
def check_code():
    code = r.lpop('to_check')
    if not code:
        return
    code_id, code_path, code_name, user_email = code.split(':')
    if not os.path.isfile(code_path):
        return
    # Посылаем на анализ - запускаем функцию или POST-запрос на API

    # Моделируем результат проверки
    result = '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
         eiusmod tempor incididunt ut labore et dolore magna aliqua.
         Ut enim ad minim veniam, quis nostrud exercitation ullamco
         laboris nisi ut aliquip ex ea commodo consequat. Duis aute
         irure dolor in reprehenderit in voluptate velit esse cillum
         dolore eu fugiat nulla pariatur. Excepteur sint occaecat
         cupidatat non proident, sunt in culpa qui officia deserunt
         mollit anim id est laborum.
    '''
    if random.random() < 0.5:
        status = CheckStatus.ACCEPTED
    else:
        status = CheckStatus.REJECTED
    check_id = save_result(
        code_id=code_id,
        result=result,
        status=status,
        sent_email=False
    )
    r.lpush(
        'to_email',
        f'{check_id}:{user_email}:{code_id}:{code_name}:{status}'
    )


@app.task
def send_email():
    code = r.lpop('to_email')
    if not code:
        return
    check_id, email, code_id, code_name, code_status = code.split(':')
    message_template = read_template(config.TEMPLATE_EMAIL)
    s = smtplib.SMTP(host=config.SMTP_HOST, port=config.SMTP_PORT)
    s.starttls()
    s.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
    msg = MIMEMultipart()
    message = message_template.substitute(
        NAME=code_name,
        STATUS=code_status,
        LINK=f'https://{config.DOMAIN}/reports/{code_id}/'
    )
    msg['From'] = config.SMTP_EMAIL
    msg['To'] = email
    msg['Subject'] = 'Ваш файл проверен'
    msg.attach(MIMEText(message, 'html')) # plain
    s.send_message(msg)
    s.quit()
    update_result(check_id)
