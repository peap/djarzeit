from datetime import datetime, timedelta

from django.db import models
from django.utils.timezone import now


class Category(models.Model):

    parent = models.ForeignKey('self',
        blank=True,
        null=True,
        db_index=True,
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
    def today(self):
        """
        Total time in this category today.
        """
        total = timedelta(0)
        for timer in self.timer_set.all():
            total += timer.today
        return total


    @property
    def last_week(self):
        """
        Total time in this category last week (a week is Monday to Sunday).
        """
        total = timedelta(0)
        for timer in self.timer_set.all():
            total += timer.last_week


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
        interval = Interval()
        interval.timer = self
        interval.save()

        self.active = True
        self.save()

    def stop(self):
        interval = Interval.objects.get(
            timer=self,
            end=None,
        )
        interval.end = now()
        interval.save()

        self.active = False
        self.save()

    @property
    def today(self):
        """
        Total time for today.
        """
        today = now()
        intervals = Interval.objects.filter(
            timer=self,
            start__year=today.year,
            start__month=today.month,
            start__day=today.day,
        )
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total.total_seconds

    @property
    def last_week(self):
        today = now()
        year, week, dow = today.isocalendar()
        if week == 1:
            last_week = 52
            year = today.year - 1
        else:
            last_week = this_week - 1
            year = today.year
        intervals = Interval.objects.filter(
            timer=self,
            start__year=year,
            week=last_week,
        )
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total


class Interval(models.Model):

    timer = models.ForeignKey('Timer')

    week = models.IntegerField(
        verbose_name='Week',
        db_index=True,
    )

    year = models.IntegerField(
        verbose_name='Year',
        db_index=True,
    )

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
        null=True,
        db_index=True,
    )

    notes = models.CharField(
        verbose_name='Notes',
        max_length=1000,
        blank=True,
        null=True,
    )

    def __init__(self, *args, **kwargs):
        today = now()
        year, week, dow = today.isocalendar()
        self.week = week
        self.year = today.year
        self.start = now()
        super().__init__(*args, **kwargs)

    @property
    def length(self):
        """
        Length of the interval. Returns datetime.timedelta object.
        """
        if self.end is None:
            length = now() - self.start
        else:
            length = self.end - self.start
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
