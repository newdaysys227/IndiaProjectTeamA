"""
Django settings for the Web Security Academy (learning edition).

このサイトは「安全でないコード」をわざと含む学習用教材です。
ローカル(127.0.0.1)でのみ動かすことを前提にしています。
絶対にインターネットへ公開しないでください。
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 学習用のため固定キー。公開環境では使わないこと。
SECRET_KEY = "django-insecure-learning-only-do-not-deploy"

from dotenv import load_env

# 脆弱性デモをそのまま見せるため DEBUG=True のまま。公開しない前提。
DEBUG = True

# ローカル専用。外部ホストは許可しない。
# プレゼン用の名前(hostsで 127.0.0.1 に向けた名前)も許可する。
# ブラウザはホスト名を小文字で送ることがあるため、両方登録する。
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "securitylabND", "securitylabnd"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "labs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 注: CsrfViewMiddleware は有効。CSRFラボの「対策前」側は @csrf_exempt で個別に無効化して見せる。
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ラボ用データ置き場（パストラバーサル等で使用）
LAB_DATA_DIR = BASE_DIR / "labs" / "lab_data"
