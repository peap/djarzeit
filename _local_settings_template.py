ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'arzeit.sqlite',
    }
}

DEBUG = True

SECRET_KEY = 'a secret key'
