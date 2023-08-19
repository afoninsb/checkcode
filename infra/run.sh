#!/bin/sh
echo "##### НАЧИНАЕМ РАБОТУ #####"
echo "### 1. Собираем статику ###"
docker-compose exec web python manage.py collectstatic --no-input
echo "+++ Статику собрали +++"
echo "### 2. Выполняем миграции ###"
docker-compose exec web python3 manage.py migrate
echo "+++ Миграции выполнили +++"
echo "### 3. Создаём суперпользователя ###"
docker-compose exec web python3 manage.py createsuperuser
echo "+++ Суперпользователя создали +++"
echo "##### РАБОТА ЗАВЕРШЕНА #####"
