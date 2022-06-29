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
    print(path_list)
    print(type(path_list))
    import math
    schedule('backup.utils.make_backups', job.destination, *path_list,
             schedule_type=Schedule.CRON, cron='* * * * SUN,TUE')
