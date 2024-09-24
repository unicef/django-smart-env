import os
import sys
from pathlib import Path

import django

here = Path(__file__).parent
sys.path.insert(0, str(here / "../src"))
sys.path.insert(0, str(here / "demoapp"))


def pytest_configure(config):
    os.environ.update(DJANGO_SETTINGS_MODULE="demo.settings")
    django.setup()
