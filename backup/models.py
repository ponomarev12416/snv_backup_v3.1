from calendar import MONDAY
from django_q.models import Schedule
from django.db import models


class Job(models.Model):

    name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=50, default='READY')
    last_run = models.CharField(max_length=200, default='')
    date_created = models.DateTimeField(
        'date created', auto_now_add=True, blank=True)
    destination = models.CharField(max_length=270*5)

    time = models.TimeField('time to start')
    MONDAY = models.BooleanField()
    TUESDAY = models.BooleanField()
    WEDNESDAY = models.BooleanField()
    THURSDAY = models.BooleanField()
    FRIDAY = models.BooleanField()
    SATURDAY = models.BooleanField()
    SUNDAY = models.BooleanField()

    schedule = models.OneToOneField(
        Schedule, on_delete=models.CASCADE, blank=True, null=True)

    def get_hours(self):
        return str(self.time.hour)

    def get_minutes(self):
        return str(self.time.minute)

    def get_hours_and_minutes(self):
        return str(self.time.hour), str(self.time.minute)

    def get_days_cron_style(self):
        """
        Returns string of days for crontab"""
        days = []
        if self.MONDAY:
            days.append('MON')
        if self.TUESDAY:
            days.append('TUE')
        if self.WEDNESDAY:
            days.append('WED')
        if self.THURSDAY:
            days.append('THU')
        if self.FRIDAY:
            days.append('FRI')
        if self.SATURDAY:
            days.append('SAT')
        if self.SUNDAY:
            days.append('SUN')
        return ','.join(days)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Repository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=250*3)
    modified = models.DateTimeField('Modified time', auto_now=True, blank=True)

    job = models.ManyToManyField(Job, related_name='repositories', blank=True)

    def __str__(self):
        return f"{self.name} : {self.path}"

    def __repr__(self):
        return self.name
