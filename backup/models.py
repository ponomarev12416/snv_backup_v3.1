from tkinter import DISABLED
import arrow
import os
from enum import Enum, auto
from datetime import datetime
from django.core.exceptions import ValidationError
from django_q.models import Schedule

from django.db import models


MAX_PATH_LENGTH = 270*5


class Status(Enum):
    READY = auto()
    RUNNING = auto()
    DISABLED = auto()


class Repository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=MAX_PATH_LENGTH)
    modified = models.DateTimeField(
        'Modified time', default=None, blank=True, null=True)

    class Meta:
        ordering = ['modified']

    def clean(self):
        if not os.path.exists(self.path):
            raise ValidationError(
                f"Path doesn't exist {self.path}",)

    def __str__(self):
        modified = None
        if self.modified:
            modified = self.modified.strftime('%c')
        return f"{self.name:<20} | {str(modified):>13}"

    def __repr__(self):
        return self.name


class Job(models.Model):
    READY = 'READY'
    RUNNING = 'RUNNING'
    DISABLED = 'DISABLED'
    STATUSES = [
        (READY, 'READY'),
        (RUNNING, 'RUNNING'),
        (DISABLED, 'DISABLED'),
    ]

    name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=50, default=READY)
    last_run = models.CharField(max_length=200, default='')
    date_created = models.DateTimeField(
        'date created', auto_now_add=True, blank=True)
    destination = models.CharField(max_length=MAX_PATH_LENGTH)

    time = models.TimeField('time to start')
    # If True, run only once no mater how many days were selected
    run_only_once = models.BooleanField(default=False)

    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    schedule = models.OneToOneField(
        Schedule, on_delete=models.CASCADE, blank=True, null=True)
    time_elapsed = models.CharField(
        'Elapsed time', max_length=5, blank=True, null=True)

    repository = models.ManyToManyField(Repository, related_name='repository')

    def clean(self):
        if not (self.monday
                or self.tuesday
                or self.wednesday
                or self.thursday
                or self.friday
                or self.saturday
                or self.sunday):
            raise ValidationError("One of the days must be chosen")
        if not self.time:
            raise ValidationError("Provide proper time")
        if not os.path.exists(self.destination):
            raise ValidationError(
                f"Path doesn't exist {self.destination}",)

    def get_hours(self):
        return self.time.hour

    def get_minutes(self):
        return self.time.minute

    def get_hours_and_minutes(self):
        return str(self.time.hour), str(self.time.minute)

    def get_days_cron_style(self):
        """
        Returns string of days for crontab"""
        days = []
        if self.monday:
            days.append('MON')
        if self.tuesday:
            days.append('TUE')
        if self.wednesday:
            days.append('WED')
        if self.thursday:
            days.append('THU')
        if self.friday:
            days.append('FRI')
        if self.saturday:
            days.append('SAT')
        if self.sunday:
            days.append('SUN')
        return ','.join(days)

    def _get_selected_days_numbers(self):
        days_of_week = [0] * 7
        if self.monday:
            days_of_week[0] = 1
        if self.tuesday:
            days_of_week[1] = 1
        if self.wednesday:
            days_of_week[2] = 1
        if self.thursday:
            days_of_week[3] = 1
        if self.friday:
            days_of_week[4] = 1
        if self.saturday:
            days_of_week[5] = 1
        if self.sunday:
            days_of_week[6] = 1
        return days_of_week

    def get_next_run(self):
        days_of_week = self._get_selected_days_numbers()
        dow = datetime.now().weekday()
        delta = 0
        if 1 in days_of_week[dow:]:
            delta = days_of_week.index(1, dow) - dow
        else:
            delta = 6 - dow + days_of_week.index(1)
        next_run = (arrow.utcnow().to('Europe/Moscow')
                    .replace(hour=self.get_hours(), minute=self.get_minutes())
                    .shift(days=delta))
        return str(next_run)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Report(models.Model):

    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField("Start Date", auto_now=True, null=True)
    destination_path = models.CharField(
        "Destination path", max_length=MAX_PATH_LENGTH)

    def __str__(self):
        return self.start.strftime('%c')
        #f'{str(self.start.year)}{str(self.start.month)}  {str(self.start.day)}'


class Track(models.Model):

    WAITING = 'WAITING'
    RUNING = 'RUNNING'
    COMPLETE = 'COMPLETE'
    FAILED = 'FAILED'
    STATE_OF_TRACK = [
        (WAITING, 'WAITING'),
        (RUNING, 'RUNNING'),
        (COMPLETE, 'COMPLETE'),
        (FAILED, 'FAILED')
    ]
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    repository_path = models.CharField(max_length=MAX_PATH_LENGTH)
    #destination_path = models.CharField(max_length=MAX_PATH_LENGTH)
    status = models.CharField(
        max_length=50, choices=STATE_OF_TRACK, default=WAITING)
    time_elapsed = models.CharField(
        'Elapsed time', max_length=5, blank=True, null=True)

    def __str__(self):
        return f"Track {self.id}"
