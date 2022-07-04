from django.db.models.signals import post_save, post_delete
from django.db import transaction
from django.dispatch import receiver
from django_q.tasks import schedule
from django_q.models import Schedule

from .models import Job, Repository
from .utils import backup


@receiver(post_delete, sender=Job)
def job_delete(sender, **kw):
    job: Job = kw['instance']
    Schedule.objects.filter(pk=job.id).delete()


@receiver(post_save, sender=Job)
def job_handler(sender, **kw):
    job: Job = kw['instance']
    transaction.on_commit(lambda: add_task(job.id))


def add_task(job_id):
    import arrow
    job: Job = Job.objects.get(pk=job_id)
    days = job.get_days_cron_style()
    hour, minutes = job.get_hours_and_minutes()
    # if job is already created and need to be updated
    if job.schedule:
        Schedule.objects.filter(pk=job.schedule.id).update(
            #next_run=job.get_next_run(),
            cron=f'{minutes} {hour} * * {days}')
    # creating a new job with new shcedule
    else:
        job.schedule = schedule('backup.utils.make_backups', job.id,
                                schedule_type=Schedule.CRON,
                                next_run=job.get_next_run(),
                                cron=f'{minutes} {hour} * * {days}')
        job.save()
