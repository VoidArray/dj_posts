Простой сайт для вывода картинок на базе Django и Redis.

### Как развернуть

Создать в папке dj_posting, рядом с настройками django, файл settings_local.py, где указать реквизиты доступа к БД.

Например:


    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


####Установить модули для Python 3

django
django-redis
pillow
requests
mysqlclient

####Запустить.