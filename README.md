[![Django-app workflow](https://github.com/G1lza92/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/G1lza92/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

# «Foodgram»

http://84.201.152.224/recipes

## Описание:
Приложение, в котором пользователи могут публиковать свои и добавлять чужие рецепты в избранное и в список покупок, подписываться на публикации других авторов. Сервис «cписок покупок» позволяет создать список из ингредиентов которые нужно купить для приготовления выбранных блюд. Есть возможность сохранить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов.
## Установка:
### После клонирования репрозитория:
* В директории infra создайте файл .env с переменными окружения для работы с базой данных (Образец файла .env.sample)
>
* Для запуска проекта выполните из директории infra команду
>
```sudo docker-compose up -d```
>
* Затем создайте суперпользователя
>
```sudo docker-compose exec web python manage.py createsuperuser```
>
### Загрузка игредиентов из CSV-файлов
```python manage.py load_data```
### Загрузка дынных без вывода в терминал
```python manage.py load_data -v 0```
>
```
Админ зона:

login: admin
password: admin

Тестовый Юзер:

login: test@test.ru
password: zxcv0987
```
### Более подробная документация со всеми адресами и доступными методами доступны по ссылке, указанной ниже:
>
### Спецификация ReDoc - [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Использованные технологии/пакеты
* [Python 3.7](https://github.com/python)
* [Django 2.2.16](https://github.com/django/django)
* [PyJWT 2.1.0](https://github.com/jpadilla/pyjwt)
* [django-filter 2.4.0](https://github.com/carltongibson/django-filter)
* [djangorestframework 3.12.4](https://github.com/encode/django-rest-framework)
* [djangorestframework-simplejwt 4.7.2](https://github.com/jazzband/djangorestframework-simplejwt)
* [drf-yasg 1.21.3](https://github.com/axnsan12/drf-yasg)
* [requests 2.26.0](https://github.com/psf/requests)
* [PostgreSQL 13.0-alpine](https://github.com/postgres/postgres)
* [Nginx 1.21.3-alpine](https://www.nginx.com/)
* [Gunicorn](https://github.com/benoitc/gunicorn)
* [Docker 20.10.21, build baeda1f](https://github.com/docker)
* [Docker-compose 3.8](https://github.com/docker)
