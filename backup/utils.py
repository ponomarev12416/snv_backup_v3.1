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
svnadmin = r"svnadmin"  # r"@SVN_BINDIR@/svnadmin"

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
    job: Job = Job.objects.get(pk=args[0])
    if job.status == Job.DISABLED:
        logger = logging.getLogger('backup')
        logger.info('Job %s is skipped, since it was disabled.' % job.name)
        return
    start_job = time.time()
    job.status = Job.READY
    job.save()
    job: Job = Job.objects.get(pk=args[0])
    repo_pathes = [rep.path for rep in job.repository.all()]
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
            job.status = 'FAILED'
            continue
        track.status = Track.COMPLETE
        track.time_elapsed = time_converter(time.time() - start)
        track.save()
    job.last_run = datetime.now()
    job.time_elapsed = time_converter(time.time() - start_job)
    if job.run_only_once == True:
        job.status = Job.DISABLED
    elif job.status == Job.RUNNING:
        job.status = Job.READY    
    job.save()


def init_report(job: Job):
    # Create initial report for current job
    report = Report.objects.create(job=job, destination_path=job.destination)
    for repository in job.repository.all():
        
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
            if (os.path.isdir(full_path) 
                and not Repository.objects.filter(path=full_path)):
                Repository.objects.create(name=obj, path=full_path)
        except Exception:
            logger = logging.getLogger('django.warning')
            logger.warning('Failde to import %s' % full_path)
            continue

def _verify(repo_dir):
    p = subprocess.Popen([svnadmin, 'verify', repo_dir],
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
        return ("Unable to verify repository '%s'"
                        ": %s" % (repo_dir, stderr_lines[0].rstrip()))

    result = ''
    for line in stdout_lines:
        result += line.decode('cp1251').strip() + '\n'
    #str_date = ' '.join(str_date[0:2])
    return result # datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')

def verify_repo(repo_dir):
    return _verify(repo_dir)