from celery import Celery

from check_tasks import config

app = Celery(
    'check_tasks',
    broker=config.REDIS_DSN,
    backend=config.REDIS_DSN,
    include=['check_tasks.tasks']
)

app.conf.update(
    result_expires=config.RESULT_EXPIRES,
)

if __name__ == '__main__':
    app.start()
