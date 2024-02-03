# Тестовое задание: Загрузка и обработка файлов

Разработать Django REST API, который позволяет загружать файлы на сервер, а затем асинхронно обрабатывать их с использованием Celery.

## Запуск:
```
docker-compose up -d
```
## Запуск тестов внутри контейнера:
```
docker exec -it storage-service-backend-1 bash
pytest
```
## Проверка покрытия тестами:
Текущее значение - 95%.
```
docker exec -it storage-service-backend-1 bash
pytest --cov
```