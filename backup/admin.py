from email.headerregistry import Group
from django.contrib import admin
from django.db import models as mdl
from django.forms import TextInput
from django.urls import path
from django.template.response import TemplateResponse

# Register your models here.

from .models import Job, Report, Track, Repository



class MembershipInline(admin.TabularInline):
    model = Repository.job.through
    extra = 1


class RepositoriesInline(admin.ModelAdmin):
    
    model = Repository
    extra = 0




class JobAdmin(admin.ModelAdmin):
    model = Job
    exclude = ['status', 'last_run', 'schedule']
    list_display = ('name', 'destination',
                     'date_created', 'last_run')

    formfield_overrides = {
        mdl.CharField: {'widget': TextInput(attrs={'size':'120'})},
    }

    inlines = [MembershipInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        

class RepositoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'path', 'modified')

    def get_list_display(self, request):
        print("ddddddsssssssssssssssssssssssssssssss")
        return super().get_list_display(request)


class ReportInline(admin.TabularInline):
    model = Track

    readonly_fields = ['repsository_path', 'destination_path']

class JobRunAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'start']
    model = Report

    inlines = [ReportInline]

    
    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Job, JobAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Report, JobRunAdmin)