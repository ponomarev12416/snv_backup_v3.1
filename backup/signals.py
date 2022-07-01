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
    path_list = [rep.path for rep in job.repositories.all()]
    days = job.get_days_cron_style()
    hour, minutes = job.get_hours_and_minutes()
    # if job is already created and need to be updated
    if job.schedule:
        Schedule.objects.filter(pk=job.schedule.id).update(
            cron=f'{minutes} {hour} * * {days}'
        )
        
    # creating a new job with new shcedule
    else:
        job.schedule = schedule('backup.utils.make_backups', job.destination, 
            *path_list, schedule_type=Schedule.CRON, 
            cron=f'{minutes} {hour} * * {days}')
        job.save()
