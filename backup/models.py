from calendar import MONDAY
from django.db import models


class Job(models.Model):

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='READY')
    last_run = models.CharField(max_length=200, default='')
    date_created = models.DateTimeField('date created', auto_now_add=True, blank=True)
    destination = models.CharField(max_length=270*5)

    def __str__(self):
        return self.name


class Schedule(models.Model):

    time = models.TimeField("time to start")
    MONDAY = models.BooleanField()
    TUESDAY = models.BooleanField()
    WEDNESDAY = models.BooleanField()
    THURSDAY = models.BooleanField()
    FRIDAY = models.BooleanField()
    SATURDAY = models.BooleanField()
    SUNDAY = models.BooleanField()

    job = models.OneToOneField(Job, on_delete=models.CASCADE)

    def __return__(self):
        self.time


class Repositories(models.Model):
    path = models.CharField(max_length=250*3)

    job = models.ManyToManyField(Job, related_name='repositories')

    def __return__(self):
        return self.path
