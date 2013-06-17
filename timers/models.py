from datetime import datetime

from django.db import models


class Category(models.Model):

    parent = models.ForeignKey('self',
        blank=True,
        null=True,
    )

    name = models.CharField(
        verbose_name='Category',
        max_length=100,
    )

    description = models.CharField(
        verbose_name='Description',
        max_length=1000,
        blank=True,
        null=True,
    )

    @property
    def timers(self):
        return Timer.objects.filter(category=self)

    @property
    def today(self):
        """
        Total time in this category today.
        """
        pass

    @property
    def last_week(self):
        """
        Total time in this category last week (a week is Monday to Sunday).
        """
        pass


class Timer(models.Model):

    category = models.ForeignKey('Category')

    name = models.CharField(
        verbose_name='Name',
        max_length=100,
    )

    description = models.CharField(
        verbose_name='Description',
        max_length=1000,
        blank=True,
        null=True,
    )

    active = models.BooleanField(
        verbose_name='Active',
        default=False,
    )

    def start(self):
        self.active = True


    def stop(self):
        self.active = False

    @property
    def today(self):
        """
        Total time for today.
        """
        today = datetime.today()
        intervals = Interval.objects().filter(
            timer=self,
            start__year=today.year,
            start__month=today.month,
            start__day=today.day,
        )
        for interval in intervals:
            total += interval.length
        return total.total_seconds

    @property
    def last_week(self):
        pass


class Interval(models.Model):

    timer = models.ForeignKey('Timer')

    start = models.DateTimeField(
        verbose_name='Start Time',
        auto_now_add=True,
    )

    end = models.DateTimeField(
        verbose_name='End Time',
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField('Tags',
        blank=True,
        null=True
    )

    notes = models.CharField(
        verbose_name='Notes',
        max_length=1000,
        blank=True,
        null=True,
    )

    @property
    def length(self):
        """
        Length of the interval. Returns datetime.datetime.
        """
        if self.end is not None:
            length = self.end - self.start
        else:
            length = datetime.now() - self.start
        return length


class Tags(models.Model):
    
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
