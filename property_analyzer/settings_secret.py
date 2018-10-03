SECRET_KEY = 'vanb&=*a841@cl#w@_9-@z&1co*!a4ll%a4r9kyx1g+58uj1(!'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'property_analyzer',
        'USER': 'Annchen',
        'PASSWORD': 'ladylexi14',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# this is to allow for different URL configs in development vs production
ROOT_URLCONF = 'property_analyzer.urls_dev'
STATIC_URL = '/static/'  ### need this for deploy; for now only have static files in getdata app but may want to change later
