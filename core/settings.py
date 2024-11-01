import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages
from celery.schedules import crontab


load_dotenv()  

BASE_DIR = Path(__file__).resolve().parent.parent


VERSION = '1.0.0'

# Security and sensitive settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG=True
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')



# Google API key
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')



ADMIN_SITE = 'mysite.admin_override.MyAdminSite'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'home',
    'quotation',
    'ministry',
    'leadership', 
    'map_app',
    'imagekit',
    'tinymce',
    'django_tables2',
    'users',
    'greetings',
    'announcement',
    'payment',
    'upcoming_event',
    'institutions',
    'django_filters', 
    'rest_framework', 
    'rest_framework_simplejwt', 
    'django_extensions',
    'django_admin_generator',
    'haystack',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'crispy_tailwind',
    'appointments',
    'newsnote',
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
    'django_ratelimit.middleware.RatelimitMiddleware',
    'users.middleware.ApprovalMiddleware',
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]





ROOT_URLCONF = 'core.urls'

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'height': '300px',
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # 'DIRS': [os.path.join(BASE_DIR, 'brothers_profile', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'announcement.context_processors.latest_news',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen insertdatetime nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code fullscreen autolink lists charmap print hr
        anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
    ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor | code |
        removeformat | inserttime preview | undo redo
    ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}



# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '3306'), 
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '28Oct',  
#         'USER': 'postgres',  
#         'PASSWORD': 'Godino$1234',  
#         'HOST': '127.0.0.1',  
#         'PORT': '5432',  
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'home/static')]
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]
STATIC_ROOT = os.path.join (BASE_DIR, 'staticfiles')

# Set the media root and URL
MEDIA_ROOT = os.path.join (BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGIN_URL = '/accounts/login/' 
LOGIN_REDIRECT_URL = '/brothers_profile/'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'users:dashboard'
LOGOUT_REDIRECT_URL = 'users:login' 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m'  
}


# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# CKEditor configurations
CKEDITOR_CONFIGS = {
    'appointment_config': {
        'toolbar': 'Custom',
        'height': 300,
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}


SITE_ID = 1


# For production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Email configuration
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')



DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Celery configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'


CELERY_BEAT_SCHEDULE = {
    'send_greetings': {
        'task': 'greetings.tasks.send_greetings',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}

# SSL Commerz configuration
SSLCOMMERZ_STORE_ID = os.getenv('SSLCOMMERZ_STORE_ID')
SSLCOMMERZ_STORE_PASS = os.getenv('SSLCOMMERZ_STORE_PASS')
SSLCOMMERZ_PAYMENT_URL = os.getenv('SSLCOMMERZ_PAYMENT_URL')
SSLCOMMERZ_VALIDATION_URL = os.getenv('SSLCOMMERZ_VALIDATION_URL')

# SSL Commerz Settings
SSLCOMMERZ_STORE_ID = 'stjos671484a36a850'
SSLCOMMERZ_STORE_PASS = 'stjos671484a36a850@ssl'  

SSLCOMMERZ_PAYMENT_URL = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'  # Sandbox
# SSLCOMMERZ_PAYMENT_URL = 'https://securepay.sslcommerz.com/gwprocess/v4/api.php'  # Production
SSLCOMMERZ_VALIDATION_URL = 'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php'



MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


INSTALLED_APPS += ['channels']

ASGI_APPLICATION = 'core.asgi.application'


# Session
# SESSION_COOKIE_AGE = 600  
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  


