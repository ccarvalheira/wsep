from django.shortcuts import render
from django.http import HttpResponse

from apps.jobs.models import Task

# Create your views here.

def task_counter(request):
    not_done = Task.objects.filter(done=False).count()
    all = Task.objects.all().count()
    return HttpResponse(str(not_done)+','+str(all))
