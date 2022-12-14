from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^-pi9ng(&g=zaka8r3%0))5n!27^_-%@-&76cu#29(zlt2ui&+'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1',
'flexroeien.up.railway.app',]
ALLOWED_ORIGINS = ['http://*', 'https://*',
'https://flexroeien.up.railway.app/admin/*',]
# CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS.copy()
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*',
'https://flexroeien.up.railway.app',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'beatrix',
    # 'debug_toolbar',
    'rest_framework',
    'corsheaders',
    ]

# AUTH_USER_MODEL = 'beatrix.User'
MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware', ## tijdens debug 
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",  #23-10-2022
    "whitenoise.middleware.WhiteNoiseMiddleware",  #22-09-22
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#  internal ips hoort bij debug toolbar
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]
ROOT_URLCONF = 'deelnamehelper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[ BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deelnamehelper.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'beatrix.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL='/images/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
    
]

# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/' # new
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
STATIC_FILES_DIR='/static'
MEDIA_ROOT= BASE_DIR / 'static/images'
FIXTURE_DIRS = [
    BASE_DIR / 'static'
    
]

CORS_ALLOW_ALL_ORIGINS=True
