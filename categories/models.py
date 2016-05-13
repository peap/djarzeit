from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    class Meta:
        ordering = ['name']

    user = models.ForeignKey(User)

    parent = models.ForeignKey(
        'self',
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

    def __str__(self):
        return self.name

    @property
    def show_in_selective_reports(self):
        for timer in self.timer_set.all():
            if timer.show_in_selective_reports:
                return True
        for category in self.category_set.all():
            if category.show_in_selective_reports:
                return True
        return False

    @property
    def is_root_category(self):
        return self.parent is None

    @property
    def root_parent(self):
        """
        The Category anscestor that is a root Category.
        """
        if self.is_root_category:
            return self
        else:
            return self.parent.root_parent

    @property
    def hierarchy_display(self):
        """
        Root Category > Child Category > This Category
        """
        if self.is_root_category:
            return self.name
        else:
            return '{0.hierarchy_display} > {1.name}'.format(self.parent, self)

    def unarchived_timers(self):
        return self.timer_set.filter(archived=False)

    def archived_timers(self):
        return self.timer_set.filter(archived=True)

    def stop_all_timers(self):
        for category in self.category_set.all():
            category.stop_all_timers()
        for timer in self.timer_set.filter(active=True):
            timer.stop()

    def get_total_time_on_date(self, date):
        total = timedelta(0)
        for category in self.category_set.all():
            total += category.get_total_time_on_date(date)
        for timer in self.timer_set.all():
            total += timer.get_total_time_on_date(date)
        return total

    def get_total_time_on_dates(self, dates):
        total = timedelta(0)
        for date in dates:
            total += self.get_total_time_on_date(date)
        return total

    def get_total_time_on_date_week(self, date):
        total = timedelta(0)
        for category in self.category_set.all():
            total += category.get_total_time_on_date_week(date)
        for timer in self.timer_set.all():
            total += timer.get_total_time_on_date_week(date)
        return total

    def get_total_time_between_dates(self, start_date, end_date):
        total = timedelta(0)
        for category in self.category_set.all():
            total += category.get_total_time_between_dates(start_date, end_date)
        for timer in self.timer_set.all():
            total += timer.get_total_time_between_dates(start_date, end_date)
        return total

    @property
    def today(self):
        """
        Total time in this category today.
        """
        total = timedelta(0)
        for category in self.category_set.all():
            total += category.today
        for timer in self.timer_set.all():
            total += timer.today
        return total

    @property
    def last_week(self):
        """
        Total time in this category last week (a week is Monday to Sunday).
        """
        total = timedelta(0)
        for category in self.category_set.all():
            total += category.last_week
        for timer in self.timer_set.all():
            total += timer.last_week
        return total
