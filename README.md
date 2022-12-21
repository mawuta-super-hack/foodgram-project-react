### Проект FoodGram - api для сайта для публикации рецептов.

***Здесь вы можете создавать рецепты, подписываться на любимых авторов, добавлять рецепты в избранное или список покупок Список покупок также доступен для скачивания.***


### Возможности API:
- Регистрация пользователя, получение или удаление токена авторизации.
- Получение списка пользователей, получение списка подписчиков.
- Получение или удаление подписки на любимых авторов.
- Получение, создание, обновление, удаление рецептов.
- Добавление рецептов в избранное или в список покупок, удаление рецепта из избранного или из списка покупок.
- Скачивание списка покупок в формате txt.


### Технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)


### Описание команд для запуска приложения локально в контейнерах с помощью Docker:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mawuta-super-hack/foodgram-poject-react.git
```

```
cd ./foodgram-poject-react/infra
```

Запуск docker-compose:
```
docker-compose up -d --build
```

Выполнение миграций:
```
docker-compose exec backend python manage.py migrate
```

Создание суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

Cбор статики:
```
docker-compose exec backend python manage.py collectstatic --no-input 
```

Создание резервной копии БД:
```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```

### Пример наполнения .env-файла:

```
DB_ENGINE=django.db.backends.postgresql <br>
DB_NAME=(имя базы данных)<br>
POSTGRES_USER=(логин для подключения к БД)<br>
POSTGRES_PASSWORD=(пароль для подключения к БД)<br>
DB_HOST=(название сервиса/контейнера)<br>
DB_PORT=(порт для подключения к БД)<br>
SECRET_KEY=(автоматически сгенерированное значение переменной при создании проекта django)<br>
```

### Импорт данных из csv для наполнения базы:

Импорт данных реализуется за счет применения миграций: 0009_add_ingredients.py и 0011_add_tags.py<br>
Путь до файлов миграций:
foodgram-project-react/backend/foodgram/foods/migrations/

### Примеры запросов к API:

- Получение списка всех категорий: <br>
GET http://localhost/api/v1/categories/

```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

- Создание рецепта: <br>
POST http://127.0.0.1:8000/api/recipes/128
```
{
  "ingredients": [
    {
      "id": 13,
      "amount": 10
    }
  ],
  "tags": [
    4
    
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Салат",
  "text": "вкусный",
  "cooking_time": 12
}
```
- Удаление рецепта (доступно для автора или администратора): <br>
DELETE http://127.0.0.1:8000/api/recipes/128



Автор проекта:
<br>
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>