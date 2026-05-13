"""
Django settings for SeeYouInside project.
Дипломный проект Некит Карины Руслановны
Колледж мировой экономики и передовых технологий
Группа: О-П-922/3
Специальность: 09.02.07 Информационные системы и программирование
2026 год
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages

# ============================================================
# БАЗОВЫЕ НАСТРОЙКИ
# ============================================================

# Корневая директория проекта
# BASE_DIR = C:\Users\nekit\Desktop\SeeYouInside
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (в продакшене должен быть скрыт в переменных окружения)
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# Режим отладки (в продакшене должно быть False)
DEBUG = True

# Разрешенные хосты (в продакшене указать домен)
ALLOWED_HOSTS = ['*']

# ============================================================
# ПРИЛОЖЕНИЯ
# ============================================================

INSTALLED_APPS = [
    # Встроенные приложения Django
    'django.contrib.admin',           # Админ-панель
    'django.contrib.auth',            # Аутентификация
    'django.contrib.contenttypes',    # Типы контента
    'django.contrib.sessions',        # Сессии
    'django.contrib.messages',        # Сообщения (уведомления)
    'django.contrib.staticfiles',    # Статические файлы
    'shop',
    
    # Сторонние приложения (можно добавить при необходимости)
    # 'debug_toolbar',                 # Панель отладки
    # 'crispy_forms',                  # Красивые формы
    # 'crispy_bootstrap5',             # Bootstrap 5 для crispy_forms
]

# ============================================================
# MIDDLEWARE (ПРОМЕЖУТОЧНОЕ ПО)
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',      # Защита от CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Дополнительные middleware
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'shop.middleware.CartMiddleware',  # Пользовательское middleware для корзины
]

# ============================================================
# URL И WSGI
# ============================================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================
# ШАБЛОНЫ
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Общие шаблоны
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # MEDIA_URL
                
                # Пользовательские контекстные процессоры
                # 'shop.context_processors.cart_count',  # Количество товаров в корзине
                # 'shop.context_processors.categories',  # Все категории для меню
            ],
            # Встроенные теги и фильтры
            'builtins': [
                'django.templatetags.static',
            ],
        },
    },
]

# ============================================================
# БАЗА ДАННЫХ
# ============================================================

# SQLite - легковесная БД, идеально для учебного проекта
# Соответствует п.1.3.2 диплома
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # Дополнительные настройки для SQLite
        'OPTIONS': {
            'timeout': 20,  # Таймаут при блокировке БД
        },
    }
}

# Для продакшена можно использовать PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'seeyouinside_db',
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# ============================================================
# ВАЛИДАЦИЯ ПАРОЛЕЙ
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================
# ИНТЕРНАЦИОНАЛИЗАЦИЯ
# ============================================================

LANGUAGE_CODE = 'ru-ru'  # Русский язык
TIME_ZONE = 'Europe/Moscow'  # Московское время
USE_I18N = True  # Интернационализация
USE_TZ = True    # Часовые пояса

# Форматы даты и времени
DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
SHORT_DATE_FORMAT = 'd.m.Y'
SHORT_DATETIME_FORMAT = 'd.m.Y H:i'

# ============================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JS, изображения)
# ============================================================

STATIC_URL = '/static/'

# Директории со статическими файлами при разработке
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Директория для собранных статических файлов (продакшен)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================
# МЕДИАФАЙЛЫ (загружаемые пользователем)
# ============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# НАСТРОЙКИ ПО УМОЛЧАНИЮ ДЛЯ МОДЕЛЕЙ
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# НАСТРОЙКИ СООБЩЕНИЙ (Bootstrap стили)
# ============================================================

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ============================================================
# НАСТРОЙКИ СЕССИЙ (для корзины)
# ============================================================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 недели (в секундах)
SESSION_COOKIE_NAME = 'seeyouinside_session'
SESSION_SAVE_EVERY_REQUEST = True

# ============================================================
# НАСТРОЙКИ КЭШИРОВАНИЯ
# ============================================================

# Для разработки используем локальный кэш в памяти
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# ============================================================
# НАСТРОЙКИ АУТЕНТИФИКАЦИИ
# ============================================================

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ============================================================
# НАСТРОЙКИ EMAIL (для отправки уведомлений)
# ============================================================

# Для разработки выводим письма в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Для продакшена:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-password'

# Email администратора
ADMINS = [
    ('Karina Nekit', 'nekit.karina@example.com'),
]
MANAGERS = ADMINS

# Email для писем от сайта
DEFAULT_FROM_EMAIL = 'noreply@seeyouinside.ru'
SERVER_EMAIL = 'server@seeyouinside.ru'

# ============================================================
# НАСТРОЙКИ ЛОГИРОВАНИЯ
# ============================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'shop': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Создаем папку для логов, если её нет
LOG_DIR = BASE_DIR / 'logs'
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

# ============================================================
# НАСТРОЙКИ БЕЗОПАСНОСТИ (для продакшена)
# ============================================================

if not DEBUG:
    # Только HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Другие заголовки безопасности
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# ============================================================
# НАСТРОЙКИ DEBUG TOOLBAR (если установлен)
# ============================================================

if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

# ============================================================
# CRISPY FORMS (если установлен)
# ============================================================

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"

import os
import dj_database_url

# Настройки для Render.com
if os.environ.get('RENDER'):
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
    
    DATABASES = {
        'default': dj_database_url.config(default='sqlite:///db.sqlite3')
    }
    
    # Статические файлы
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')