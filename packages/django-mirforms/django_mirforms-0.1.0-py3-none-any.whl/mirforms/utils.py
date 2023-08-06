from django.conf import settings
import cryptocode


def encode(text, key=None):
    if not key:
        key = settings.SECRET_KEY

    return cryptocode.encrypt(text, key)


def decode(text, key=None):
    if not key:
        key = settings.SECRET_KEY

    return cryptocode.decrypt(text, key)
