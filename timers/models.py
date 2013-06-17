from django.db import models


class Timer(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=100,
    )


class Interval(models.Model):

    timer = models.ForeignKey('Timer')

    start = models.DateTimeField(
        verbose_name='Start Time',
    )

    end = models.DateTimeField(
        verbose_name='End Time',
    )

    tags = models.ManyToManyField('Tags')

    notes = models.CharField(
        verbose_name='Notes',
        max_length=1000,
    )


class Tags(models.Model):
    
    name = models.CharField(
        verbose_name='Name',
        max_length=25,
    )
