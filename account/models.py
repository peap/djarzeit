import pytz

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    TZ_CHOICES = tuple((tz, tz) for tz in pytz.common_timezones)

    user = models.OneToOneField(User)

    timezone = models.CharField(
        max_length=50,
        choices=TZ_CHOICES,
        verbose_name='Timezone',
    )
