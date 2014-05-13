from django.db import models
from django.utils.timezone import datetime, now, timedelta

from categories.models import Category
from tags.models import Tag


class Timer(models.Model):

    class Meta:
        ordering = ['name']

    category = models.ForeignKey(Category)

    name = models.CharField(
        verbose_name='Name',
        max_length=100,
    )

    active = models.BooleanField(
        verbose_name='Active',
        default=False,
    )

    archived = models.BooleanField(
        verbose_name='Archived',
        default=False,
    )

    def __str__(self):
        return self.name

    def start(self):
        self.category.root_parent.stop_all_timers()

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
    def intervals_today(self):
        today = now()
        today_midnight = datetime(today.year, today.month, today.day)
        return Interval.objects.filter(
            timer=self,
            start__gt=today_midnight,
        )

    @property
    def today(self):
        """
        Total time for today as a datetime.timedelta object.
        """
        intervals = self.intervals_today
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total

    @property
    def last_week(self):
        """
        Total time for last_week as a datetime.timedelta object.
        """
        year, week, dow = (now() - timedelta(days=7)).isocalendar()
        intervals = Interval.objects.filter(
            timer=self,
            start__year=year,
            week=week,
        )
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total


class Interval(models.Model):

    class Meta:
        ordering = ['-start']

    timer = models.ForeignKey(Timer)

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

    tags = models.ManyToManyField(Tag,
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
        kwargs['week'] = week
        kwargs['year'] = today.year
        kwargs['start'] = now()
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
