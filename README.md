# Тестовое задание "Проверка кода"


## Стек технологий

Python 3.10, Django 4.2, PostgreSQL 15, nginx 1.25, Redis, Celery, Docker, Docker-compose


## Локальный запуск

Клонируйте код проекта на свой компьютер:

```bash
  git clone git@github.com:afoninsb/checkcode.git
```
Перейдите в папку '/infra/', переименуйте в ней файл .env.dist в .env и отредактируйте его содержимое (при необходимости):

```bash
DEBUG=False
SECRET_KEY=django-in3rdfcure-k%otdfdvsdfdfgggfg6iqfu&y6yy!ci%s_&3mg5p
DOMAIN=127.0.0.1:8000
REDIS_DSN=redis://172.30.0.2:6379
REDIS_HOST=redis
REDIS_PORT=6379
SMTP_HOST=smtp.mail.com
SMTP_PORT=2525
SMTP_EMAIL=name@mail.ru
SMTP_PASSWORD=Pass123!
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

Запустите терминал, перейдите в папку '/infra/' и запустите docker-compose:

```bash
  cd <путь_до_папки_проекта>/checkcode/infra
  docker-compose up --build
```

Запустите ещё один терминал, перейдите в папку '/infra/' и запустите скрипт run.sh:
```bash
  cd <путь_до_папки_проекта>/checkcode/infra
  sh run.sh
```
Скрипт выполнит следующие действия:
  - Соберёт статику
  - Выполнит миграции
  - Создаст суперпользователя


## Адреса

http://127.0.0.1/admin/ -админпанель Django

http://127.0.0.1/ - сайт


## Очистка компьютера

После теста приложения вы можете очистить свой компьютер от созданных приложением артефактов: контейнеров, образов, томов.

Запустите терминал, перейдите в папку '/infra/' и запустите скрипт clean.sh:
```bash
  cd <путь_до_папки_проекта>/company/infra
  sh clean.sh
```


## Контакты

[Вопросы лучше задавать в Telegram @afoninsb](https://t.me/afoninsb)

[Можно написать на почту afoninsb@yandex.ru](mailto:afoninsb@yandex.ru)
