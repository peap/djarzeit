from django.db import models


class Timer(models.Model):

    name = models.CharField(
        verbose_name='Name',
        max_length=100,
    )

    active = models.BooleanField(
        verbose_name='Active',
        default=False,
    )

    def start(self):
        self.active = True


    def stop(self):
        self.active = False


class Interval(models.Model):

    timer = models.ForeignKey('Timer')

    start = models.DateTimeField(
        verbose_name='Start Time',
    )

    end = models.DateTimeField(
        verbose_name='End Time',
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField('Tags')

    notes = models.CharField(
        verbose_name='Notes',
        max_length=1000,
    )

    @property
    def length(self):
        return (self.end - self.start)


class Tags(models.Model):
    
    name = models.CharField(
        verbose_name='Name',
        max_length=25,
    )
