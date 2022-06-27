from email.headerregistry import Group
from django.contrib import admin

# Register your models here.

from .models import Job, Repositories, Schedule


class MembershipInline(admin.TabularInline):
    model = Repositories.job.through
    extra = 1


class RepositoriesInline(admin.ModelAdmin):
    model = Repositories
    extra = 0


class ScheduleAdmin(admin.StackedInline):
    model =Schedule

class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'destination']}),
    ]


    inlines = [ScheduleAdmin, MembershipInline]


admin.site.register(Job, JobAdmin)
admin.site.register(Schedule)
admin.site.register(Repositories)
