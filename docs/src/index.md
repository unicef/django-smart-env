---
title: Documentation
---

django-smart-env is a small add-on to the [django-environ](https://django-environ.readthedocs.io/en/latest/) 
package django-smart-env is a small add-on to the [django-environ](https://django-environ.readthedocs.io/en/latest/) 
package that adds some extra features.

- extend configuration
- management command
- django check framework integration


## Install

    pip install django-smart-env

Create a `config.py` in your project root with:

    CONFIG = {"DEBUG": (bool, False, True, False, "Enable/Disable debug mode",
              "DATABASE_URL": (str, "", "", True, "Database connection URL style"
              }
    env = SmartEnv(**CONFIG)


In your `settings.py`:
    
    from <app>.config import env

    INSTALLED_APPS = [
        ...
        "smart_env"
    ]

    DEBUG = env("DEBUG")
    DATABASES = {"default": env("DATABASE_URL")} 

Check your configuration

    python manage.py check


Dump you configuration

    python manage.py env
