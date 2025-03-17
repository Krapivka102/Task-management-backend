import os

from config.django.base import BASE_DIR
from config.env import env

env.read_env(os.path.join(BASE_DIR, '.env'))

DATABASE_ENGINE = env('ENGINE', default='django.db.backends.sqlite3')

if DATABASE_ENGINE == 'django.db.backends.postgresql':
    try:
        import psycopg2

        connection = psycopg2.connect(
            dbname=env('POSTGRES_DB'),
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            host=env('POSTGRES_HOST'),
            port=5432,
        )
        connection.close()

        DATABASES = {
            'default': {
                'ENGINE': DATABASE_ENGINE,
                'NAME': env('POSTGRES_DB', default='web_db_pg'),
                'USER': env('POSTGRES_USER', default='postgres'),
                'PASSWORD': env('POSTGRES_PASSWORD', default='postgres'),
                'HOST': env('POSTGRES_HOST', default='web_db_pg'),
                'PORT': 5432,
            }
        }
    except (ImportError, psycopg2.OperationalError):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
