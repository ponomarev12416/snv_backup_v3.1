from calendar import MONDAY
from django.core.exceptions import ValidationError
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
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()

    schedule = models.OneToOneField(
        Schedule, on_delete=models.CASCADE, blank=True, null=True)

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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class CustomSchedule(Schedule):

    class Meta:
        proxy = True


class Repository(models.Model):
    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=250*3)
    modified = models.DateTimeField('Modified time', auto_now=True, blank=True)

    job = models.ManyToManyField(Job, related_name='repositories', blank=True)

    def __str__(self):
        return f"{self.name} : {self.path}"

    def __repr__(self):
        return self.name

class JobRun(models.Model):

    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=False)
    start = models.DateTimeField("Date")



class Report(models.Model):

    job_run = models.ForeignKey(JobRun, on_delete=models.CASCADE, editable=False)
    repsository_path = models.CharField(max_length=270*3)
    destination_path = models.CharField(max_length=270*3)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Report {self}"




