import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'dyai!1#d%#@t1kw6#bp)8qy6bso8k=1$)6(==g0wdi*$@_cu35'

DEBUG = True
