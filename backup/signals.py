from django.db.models.signals import post_save, pre_init
from django.db import transaction
from django.dispatch import receiver
from django_q.tasks import schedule
from django_q.models import Schedule

from .models import Job, Repository
from .utils import backup


@receiver(post_save, sender=Job)
def job_handler(sender, **kw):
    job: Job = kw['instance']
    transaction.on_commit(lambda: add_task(job.id))




def add_task(arg):
    job: Job = Job.objects.get(pk=arg)
    path_list = []
    for rep in job.repositories.all():
        path_list.append(rep.path)
    days = job.get_days_cron_style()
    hour = job.get_hours()
    minutes = job.get_minutes()
    
    if job.schedule:
        #x = Schedule.objects.get(pk=job.schedule.id)
        schedule_ = schedule('backup.utils.make_backups', job.destination, *path_list,
             schedule_type=Schedule.CRON, cron=f'{minutes} {hour} * * {days}')
        Schedule.objects.filter(pk=job.schedule.id).update(schedule_)
    else:
        job.schedule = schedule('backup.utils.make_backups', job.destination, *path_list,
             schedule_type=Schedule.CRON, cron=f'{minutes} {hour} * * {days}')
        job.save()

