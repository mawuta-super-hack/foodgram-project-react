### Проект FoodGram - api для сайта для публикации рецептов.

***Здесь вы можете создавать рецепты, подписываться на любимых авторов, создавать и выгружать списки покупок.***


<br>

![workflow](https://github.com/mawuta-super-hack/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?)

### Возможности API:
- Регистрация и выыдача токена авторизации.
- Получение, создание, удаление учетных записей.
- Получение, создание, обновление, удаление рецептов.
- Добавление рецептов в избранное, в список покупок.
- Подписка на любимых авторов.


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mawuta-super-hack/foodgram-project-react.git
```

Выполение миграций:
```
python manage.py migrate
```

Создание суперпользователя:
```
python manage.py createsuperuser
```

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


Автор проекта:
<br>
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>

Данные администратора:
email: maria@mail.ru
password: maria

