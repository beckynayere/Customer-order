import os
from pathlib import Path
import dj_database_url
from decouple import config

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-p8b8^4qe%wuuc8n&vnwb=-68=tdf*2l^%xo#9d&mc8b(syg8i&')

DEBUG = config('DJANGO_DEBUG', default='True') == 'True'

ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='').split(',')




# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'oauth2_provider',
    'oidc_provider',  
    'orders',  # Your orders app
    'mozilla_django_oidc',
    # Third-party apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'customer_order_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'customer_order_service.wsgi.application'

# DATABASES = {
#     'default': dj_database_url.config(
#         default=config(
#             'DATABASE_URL',
#             default='postgresql://customer_orders_user:KGWbmW3XYoXr3Kir26exF4mJNk5DCLlw@dpg-csvij9aj1k6c73c735dg-a/customer_orders'
#         )
#     )
# }

DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',  # Use a single DATABASE_URL environment variable for the full connection string
            default='postgresql://customer_orders_user:KGWbmW3XYoXr3Kir26exF4mJNk5DCLlw@dpg-csvij9aj1k6c73c735dg-a/customer_orders'
        )
    ),
    'backup': {  # Fallback for explicit field-based config
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='customer_orders'),
        'USER': config('POSTGRES_USER', default='customer_orders_user'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='KGWbmW3XYoXr3Kir26exF4mJNk5DCLlw'),
        'HOST': config('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    },
}   
# Authentication
AUTHENTICATION_BACKENDS = [
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Login and logout redirects
LOGIN_REDIRECT_URL = '/'  
LOGOUT_REDIRECT_URL = '/'  

SITE_ID = 1

# Email settings for account verification (optional)
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "optional"

# OIDC Configuration
OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID', 'zxC8Uvva3Ygsbo47cWBuoGcxHIGqiwlJ')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET', '7g5Lh8R6H4EcI_V1RgNnfe0u5AKYqLLfXNiKrlQnlcTd1wQduw6NrZTbHC3TEAyX')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv('OIDC_OP_AUTHORIZATION_ENDPOINT', 'https://your-oidc-provider/authorize')
OIDC_OP_TOKEN_ENDPOINT = os.getenv('OIDC_OP_TOKEN_ENDPOINT', 'https://your-oidc-provider/token')
OIDC_OP_USER_ENDPOINT = os.getenv('OIDC_OP_USER_ENDPOINT', 'https://your-oidc-provider/userinfo')
OIDC_OP_LOGOUT_ENDPOINT = os.getenv('OIDC_OP_LOGOUT_ENDPOINT', 'https://your-oidc-provider/logout')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files for deployment
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
