# praktikum_new_diplom
python -m venv venv
pip install -r reqierements.txt 
source venv/Scripts/activate 
1. django-admin startproject foodgram 
2. python manage.py startapp api // users // foods
3. ALLOWED_HOSTS = ['*'] // leng 'ru-RU'

    INSTALLED_APPS = [
    'api.apps.ApiConfig', // ... ]
4. add api/urls /// 
5. Описание моделей 
models - settings.py - media = '/media/; media_root = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
urls +  импорт сеттингс и статик
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
AUTH_USER_MODEL = 'users.User' settings
6. Описание админки 
7. Миграции, создание суперюзера, запуск проекта
maria@mail.ru ma ria qazxsw21
для токена устновли дьезер зарегали в сетингах,  resf - frame : def perm cls def auth cls миграции 
