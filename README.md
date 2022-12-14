### Проект FoodGram - api для сайта для публикации рецептов.

***Здесь вы можете создавать рецепты, подписываться на любимых авторов, создавать и выгружать списки покупок.***


<br>

![workflow](https://github.com/mawuta-super-hack/foodgram-poject-react/actions/workflows/yamdb_workflow.yml/badge.svg?)

### Возможности API:
- Регистрация и выыдача токена авторизации.
- Получение, создание, удаление учетных записей.
- Получение, создание, обновление, удаление рецептов.
- Добавление рецептов в избранное, в список покупок.
- Подписка на любимых авторов.


### Описание команд для запуска приложения в контейнерах:

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

Выполение миграций:
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

### Пример наполения .env-файла:

DB_ENGINE=django.db.backends.postgresql <br>
DB_NAME=(им базы данных)<br>
POSTGRES_USER=(логин для подключения к БД)<br>
POSTGRES_PASSWORD=(пароль для подключения к БД)<br>
DB_HOST=(название сервиса/контейнера)<br>
DB_PORT=(порт для подключения к БД)<br>
SECRET_KEY=(автоматически сгенерированное значение переменной при создании проекта django)<br>

### Импорт данных из csv для наполнения базы:

Реализуется за счет применения миграции: 0009_add_ingredients.py

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



Полный список запросов и эндпоинтов описан в документации ReDoc.
Документация доступна после запуска проекта по [адресу](http://51.250.26.79/docs).

<br>
Проект доступен по [адресу](http://51.250.26.79/recipes).
<br>

Автор проекта:
<br>
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>

<br>
Данные администратора:

<br>
email: maria@mail.ru

<br>
password: maria

