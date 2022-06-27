from email.headerregistry import Group
from django.contrib import admin
from django.db import models as mdl
from django.forms import TextInput

# Register your models here.

from .models import Job, Repository


class MembershipInline(admin.TabularInline):
    model = Repository.job.through
    extra = 1


class RepositoriesInline(admin.ModelAdmin):
    model = Repository
    extra = 0


class JobAdmin(admin.ModelAdmin):
    model = Job
    exclude = ['status', 'last_run']
    list_display = ('name', 'destination',
                     'date_created', 'last_run')

    formfield_overrides = {
        mdl.CharField: {'widget': TextInput(attrs={'size':'120'})},
    }

    inlines = [MembershipInline]


admin.site.register(Job, JobAdmin)
admin.site.register(Repository)
