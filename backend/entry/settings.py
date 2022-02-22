"""
Django 4
"""

import os
from pathlib import Path

from utils.logs import get_logging_config_dict
from utils.tools import getenv_or_raise

# 目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 环境配置
try:
    with open(os.path.join(BASE_DIR, "env"), "r", encoding="utf-8") as env_setting_file:
        while True:
            env_setting = env_setting_file.readline()
            if env_setting:
                key, val = env_setting.strip("\n").split("=")
                os.environ[key] = val
            else:
                break
except FileNotFoundError:
    pass

# DEBUG
DEBUG = True if os.getenv("DEBUG", "False") == "True" else False

# APP_CODE & SECRET
APP_CODE = getenv_or_raise("APP_CODE")
SECRET_KEY = getenv_or_raise("APP_SECRET_KEY")
APP_SECRET = SECRET_KEY

# 允许的host
ALLOWED_HOSTS = [getenv_or_raise("BACKEND_HOST")]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", True)
CORS_ORIGIN_WHITELIST = [getenv_or_raise("FRONTEND_URL")]
CSRF_TRUSTED_ORIGINS = [getenv_or_raise("FRONTEND_URL")]

# APPs
INSTALLED_APPS = [
    "corsheaders",
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.account",
    "apps.circle",
]

# 中间件
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "utils.middlewares.CSRFExemptMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "utils.middlewares.SQLDebugMiddleware",
    "utils.middlewares.UnHandleExceptionMiddleware",
]

# 路由
ROOT_URLCONF = "entry.urls"

# 模板
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "entry.wsgi.application"

# 数据库与缓存
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv_or_raise("DB_NAME"),
        "USER": getenv_or_raise("DB_USER"),
        "PASSWORD": getenv_or_raise("DB_PASSWORD"),
        "HOST": getenv_or_raise("DB_HOST"),
        "PORT": int(getenv_or_raise("DB_PORT")),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REDIS_HOST = getenv_or_raise("REDIS_HOST")
REDIS_PORT = int(getenv_or_raise("REDIS_PORT"))
REDIS_PASSWORD = getenv_or_raise("REDIS_PASSWORD")
REDIS_DB = int(getenv_or_raise("REDIS_DB"))
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    }
}

# 用户认证
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 国际化
LANGUAGE_CODE = os.getenv("DEFAULT_LANGUAGE", "zh-Hans")
TIME_ZONE = os.getenv("DEFAULT_TIME_ZONE", "Asia/Shanghai")
USE_I18N = True
USE_L10N = True
USE_TZ = False
LANGUAGES = (("zh-hans", "中文简体"),)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# 静态文件
STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Session
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", f"{APP_CODE}-sessionid")
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 60 * 60 * 24 * int(os.getenv("SESSION_COOKIE_AGE", 365))
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN")

# 日志
LOG_LEVEL = "INFO"
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = get_logging_config_dict(LOG_LEVEL, LOG_DIR)

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["utils.renderers.APIRenderer"],
    "DEFAULT_PAGINATION_CLASS": "utils.paginations.NumPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_THROTTLE_RATES": {"login_scope": "3/m"},
    "EXCEPTION_HANDLER": "utils.exceptions.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.authenticators.SessionAuthenticate",
    ],
    "DEFAULT_CHARSET": "utf8mb4",
}

# Admin Site
SIMPLEUI_INDEX = getenv_or_raise("FRONTEND_URL")
SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_TITLE = "Time Circle"
SIMPLEUI_LOGO = "https://public.incv.net/favicon.ico"
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_ICON = {}
SIMPLEUI_CONFIG = {"system_keep": False}
