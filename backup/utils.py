import os
import subprocess
import time
import logging

from datetime import datetime

from backup.temp import time_converter


from .backuper import backup as backup
from .models import Job, Report, Repository, Track
#from .temp import backup


# Path to svnlook utility
svnlook = r"svnlook"  # r"@SVN_BINDIR@/svnlook"


def get_date_modified(repo_dir):
    """Examine the repository REPO_DIR using the svnlook binary
    specified by SVNLOOK, and return the date modified."""

    p = subprocess.Popen([svnlook, 'date', repo_dir],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    infile, outfile, errfile = p.stdin, p.stdout, p.stderr

    stdout_lines = outfile.readlines()
    stderr_lines = errfile.readlines()
    outfile.close()
    infile.close()
    errfile.close()

    if stderr_lines:
        raise Exception("Unable to find the youngest revision for repository '%s'"
                        ": %s" % (repo_dir, stderr_lines[0].rstrip()))

    str_date = stdout_lines[0].decode('cp1251').strip().split(' ')
    
    return datetime.strptime(' '.join(str_date[0:2]), '%Y-%m-%d %H:%M:%S')



def update_repos_meta():
    repositories = Repository.objects.all()
    for repo in repositories:
        try:
            repo.modified = get_date_modified(repo.path)
        except Exception:
            logger = logging.getLogger('django.warning')
            logger.warning('Failed to get date of last modification %s' % repo.path)
            repo.modified = None
        repo.save()


def make_backups(*args):
    start_job = time.time()
    job: Job = Job.objects.get(pk=args[0])

    repo_pathes = [rep.path for rep in job.repositories.all()]
    report = init_report(job)
    for repo_path in repo_pathes:
        start = time.time()
        track: Track = (Track.objects
            .filter(report=report.id)
            .filter(repository_path=repo_path)[0])
        track.status = Track.RUNING
        track.save()
        try:
            backup(repo_path, job.destination)
        except Exception as e:
            logger = logging.getLogger('django.warning')
            logger.warning('Failed to backup %s to %s' % (repo_path, job.destination))
            track.status = Track.FAILED
            track.time_elapsed = time_converter(time.time() - start)
            track.save()
            continue
        track.status = Track.COMPLETE
        track.time_elapsed = time_converter(time.time() - start)
        track.save()
    job.last_run = datetime.now()
    job.time_elapsed = time_converter(time.time() - start_job)
    job.save()


def init_report(job: Job):
    # Create initial report for current job
    report = Report.objects.create(job=job, destination_path=job.destination)
    for repository in job.repositories.all():
        
        try:
            Track.objects.create(
                report=report,
                repository_path=repository.path)
        except Exception:
            logger = logging.getLogger('django.warning')
            logger.warning('Failed to write the Track %s : %s' % (report, repository.path))
            continue
    return report
    

def scan_for_repos(path):
    from .models import Repository
    for obj in os.listdir(path):
        try:
            full_path = os.path.join(path, obj)
            if (os.path.islink(full_path) 
                and not Repository.objects.filter(path=full_path)):
                Repository.objects.create(name=obj, path=full_path)
        except Exception:
            logger = logging.getLogger('django.warning')
            logger.warning('Failde to import %s' % full_path)
            continue