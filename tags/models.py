from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):

    user = models.ForeignKey(User)
        
    name = models.CharField(
        verbose_name='Name',
        max_length=25,
    )

    description = models.CharField(
        verbose_name='Description',
        max_length=1000,
        blank=True,
        null=True,
    )
