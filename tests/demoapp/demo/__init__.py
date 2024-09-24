from smart_env import SmartEnv

CONFIG = {
    "DEBUG": (bool, False, True, False, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug"),
    "DATABASE_URL": (str, "",  "sqlite:///demo.db", True, "https://docs.djangoproject.com/en/5.1/ref/settings/#DATABASES"),
    "USE_TZ": (bool, True, True, False, "https://docs.djangoproject.com/en/5.1/ref/settings/#debug"),
    "SECURE_SSL_REDIRECT": (bool, True, False, False,"https://docs.djangoproject.com/en/5.1/ref/settings/#SECURE_SSL_REDIRECT"),
    "SESSION_COOKIE_SECURE": (bool, True, False, False, "https://docs.djangoproject.com/en/5.1/ref/settings/#SESSION_COOKIE_SECURE"),
}

env = SmartEnv(**CONFIG)
