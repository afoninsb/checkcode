#!/bin/sh
docker stop infra_celery_1 infra_nginx_1 infra_web_1 infra_redis_1 infra_db_1
docker rm infra_celery_1 infra_nginx_1 infra_web_1 infra_redis_1 infra_db_1
docker rmi infra_web infra_celery redis nginx postgres
volume rm infra_media_volume infra_postgres_valume infra_static_volume
