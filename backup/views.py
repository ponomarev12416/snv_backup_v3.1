from django.http import Http404
from django.shortcuts import render, redirect

import backup.config as config
from .utils import scan_for_repos
from .models import Job

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