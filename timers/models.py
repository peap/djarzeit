import pytz

from django.db import models
from django.utils.timezone import datetime, now, timedelta

from categories.models import Category


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

        interval = Interval(timer=self)
        interval.save()

        self.active = True
        self.save()

    def stop(self):
        interval = self.interval_set.get(
            end=None,
        )
        interval.end = now()
        interval.save()

        self.active = False
        self.save()

    def archive(self):
        self.archived = True
        self.save()

    def unarchive(self):
        self.archived = False
        self.save()

    def get_intervals_on_date(self, date):
        user_tz = pytz.timezone(self.category.user.profile.timezone)
        local_date = user_tz.normalize(date.astimezone(user_tz))
        local_date_start = datetime(
            local_date.year, local_date.month, local_date.day, 0, 0, 0)
        local_date_end = datetime(
            local_date.year, local_date.month, local_date.day, 23, 59, 59)
        return self.interval_set.filter(
            start__range=(local_date_start, local_date_end),
        )

    def get_intervals_on_date_week(self, date):
        user_tz = pytz.timezone(self.category.user.profile.timezone)
        local_date = user_tz.normalize(date.astimezone(user_tz))
        year, week, dow = local_date.isocalendar()
        return self.interval_set.filter(
            start__year=year,
            week=week,
        )

    def get_total_time_on_date(self, date):
        intervals = self.get_intervals_on_date(date)
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total

    def get_total_time_on_date_week(self, date):
        intervals = self.get_intervals_on_date_week(date)
        total = timedelta(0)
        for interval in intervals:
            total += interval.length
        return total

    @property
    def intervals_yesterday(self):
        yesterday = now() - timedelta(days=1)
        return self.get_intervals_on_date(yesterday)

    @property
    def intervals_today(self):
        return self.get_intervals_on_date(now())

    @property
    def yesterday(self):
        """
        Total time for today as a datetime.timedelta object.
        """
        yesterday = now() - timedelta(days=1)
        return self.get_total_time_on_date(yesterday)

    @property
    def today(self):
        """
        Total time for today as a datetime.timedelta object.
        """
        return self.get_total_time_on_date(now())

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

    @property
    def hierarchy_display(self):
        return '{0} :: {1}'.format(self.category.hierarchy_display, self)


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
        end = self.end if self.end is not None else now()
        return end - self.start

    @classmethod
    def user_intervals(cls, user):
        return cls.objects.filter(timer__category__user=user)

    def active_at(self, dt):
        active = False
        if self.start <= dt:
            if self.end is None:
                active = dt <= now()
            else:
                active = self.end >= dt
        return active


