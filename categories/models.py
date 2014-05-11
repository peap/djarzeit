from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    user = models.ForeignKey(User)

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

    def stop_all_timers(self):
        for category in self.category_set.all():
            category.stop_all_timers()
        for timer in self.timer_set.filter(active=True):
            timer.stop()

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
