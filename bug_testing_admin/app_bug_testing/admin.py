from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import BugReport, FileReport


class FileReportInline(admin.StackedInline):
    model = FileReport


class BugReportAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'device_model', 'periodicity', 'type_of_problem', 'title', 'created_at'
    ]
    list_display_links = [
        'username', 'device_model', 'periodicity', 'type_of_problem', 'title', 'created_at'
    ]
    list_filter = ['title', 'type_of_problem', 'periodicity', 'created_at']
    inlines = [FileReportInline]


class FileReportAdmin(admin.ModelAdmin):
    list_display = ['report', 'file']
    list_display_links = ['report']
    list_filter = ['report']


admin.site.register(BugReport, BugReportAdmin)
admin.site.register(FileReport, FileReportAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
