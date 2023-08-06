# После установки

Добавить приложения в список **INSTALLED_APPS** в settings.py
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'sso_server'
]
```

Добавить в settings.py переменную, содержащую корневой домен для установки cookies

```python
DOMAIN = '.local'
```

Выполнить миграции:
```shell
python manage.py migrate
```

**Добавить в settings.py в middleware:**
```'sso_server.middleware.UserCookieMiddleWare'```

Добавить в urls.py следующий маршрут:

```python
urlpatterns = [
    ...
    path('sso/', include('sso_server.urls'))
]
```