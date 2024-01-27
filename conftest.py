import pytest
from django.conf import settings

from blogapi.env import *


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": bdEngine,
        "NAME": bdName,
        "USER": bdUser,
        "PASSWORD": bdPass,
        "HOST": bdHost,
        "PORT": bdPort,
    }
