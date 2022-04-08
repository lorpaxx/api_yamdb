# YaMDb API
## Проект YaMDb собирает отзывы пользователей на различные произведения.
### Технологии в проекте:
- Python 3.9
- Django 2.2.16
- Django REST Flamework
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Gena40/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
### Как регистрировать пользователей:
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами *email* и *username* на [эндпоинт](/api/v1/auth/signup).
2. **YaMDB** отправляет письмо с кодом подтверждения (```confirmation_code```) на адрес *email*.
3. Пользователь отправляет POST-запрос с параметрами *username* и *confirmation_code* на [эндпоинт](/api/v1/auth/token/), в ответе на запрос ему приходит *token* (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на [эндпоинт](/api/v1/users/me/) и заполняет поля в своём профайле (описание полей — в документации).

### Дополнительно:
- запросы к API начинаются с ```/api/v1/```
- в проекте доступно OpenAPI specification в формате ReDoc.

# Авторы
Проект совместный, оригинальная ссылка:
https://github.com/Gena40/yamdb-api

