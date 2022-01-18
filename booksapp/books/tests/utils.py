from random import randint

from django.utils import timezone


def set_random_date():
    return timezone.now() + timezone.timedelta(days=randint(1, 200))