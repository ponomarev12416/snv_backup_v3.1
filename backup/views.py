from datetime import datetime
from django.http import Http404
from django.shortcuts import render, redirect

import backup.config as config
from .utils import scan_for_repos, verify_repo
from .models import Job, Repository

def index(request):
    for path in config.repo_path:
        scan_for_repos(path)   
    return redirect('/admin/backup/repository')


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'backup/detail.html', {'job': job})


def verify(request):
    repositories = Repository.objects.all()
    with open('report.txt', 'w') as f:
        f.write('\n' + datetime.now().strftime("%c"))
        for repo in repositories:
            s = f'\n{repo.name:<20} \n{verify_repo(repo.path)}'
            f.write(s)
    return redirect('/admin/backup/repository')
