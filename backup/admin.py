from email.headerregistry import Group
from django.contrib import admin
from django.db import models as mdl
from django.forms import TextInput
from django.urls import path
from django.template.response import TemplateResponse
from django_q.tasks import Chain

# Register your models here.

from .models import Job, Report, Track, Repository
from .utils import update_repos_meta, make_backups



@admin.action(description='Run selected jobs')
def run_jobs(modeladmin, request, queryset):
    chain = Chain(cached=True)
    for job in queryset:
        chain.append('backup.utils.make_backups', job.id)
    chain.run()


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
        mdl.CharField: {'widget': TextInput(attrs={'size': '120'})},
    }

    inlines = [MembershipInline]
    actions = [run_jobs]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class RepositoryAdmin(admin.ModelAdmin):

    search_fields = ['name']

    list_display = ('name', 'path', 'modified')
    exclude = ['modified']

    # A template for a very customized change view:
    #change_form_template = 'admin/ba/extras/openstreetmap_change_form.html'

    def get_osm_info(self):
        update_repos_meta()

    def changelist_view(self, request, extra_context=None):
        # return super().changelist_view(request, extra_context)
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_osm_info()
        return super().changelist_view(request, extra_context)


class ReportInline(admin.TabularInline):
    model = Track
    extra = 0

    readonly_fields = ['status', 'repository_path']


class JobRunAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'start', 'destination_path']
    list_display = ('job', 'start', 'destination_path')
    model = Report

    inlines = [ReportInline]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Job, JobAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Report, JobRunAdmin)
