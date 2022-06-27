from django.http import HttpResponse,Http404
from django.template import loader
from django.shortcuts import render

from .models import Job

def index(request):
    latest_job_list = Job.objects.all()
    output = ', '.join([q.name for q in latest_job_list])
    template = loader.get_template('backup/index.html')
    context = {
        'latest_job_list': latest_job_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'backup/detail.html', {'job': job})