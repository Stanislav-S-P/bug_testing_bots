from django.contrib import admin
from .models import *


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


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'email', 'device_model', 'login', 'hash_password', 'status', 'created_at']
    list_display_links = [
        'user_id', 'username', 'email', 'device_model', 'login', 'hash_password', 'status', 'created_at'
    ]
    list_filter = ['created_at', 'status']

    actions = ['mark_as_new', 'mark_as_activity', 'mark_as_blocked']

    def mark_as_new(self, request, queryset):
        queryset.update(status='Новый')

    def mark_as_activity(self, request, queryset):
        queryset.update(status='Активный')

    def mark_as_blocked(self, request, queryset):
        queryset.update(status='Заблокирован')

    mark_as_new.short_description = 'Перевести в статус Новый'
    mark_as_activity.short_description = 'Перевести в статус Активный'
    mark_as_blocked.short_description = 'Перевести в статус Заблокирован'


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id']
    list_display_links = ['user_id']


class CommandActivityAdmin(admin.ModelAdmin):
    list_display = ['command', 'status']
    list_display_links = ['command', 'status']

    actions = ['mark_as_open', 'mark_as_close']

    def mark_as_open(self, request, queryset):
        queryset.update(status='Открыта')

    def mark_as_close(self, request, queryset):
        queryset.update(status='Закрыта')

    mark_as_open.short_description = 'Перевести в статус Открыта'
    mark_as_close.short_description = 'Перевести в статус Закрыта'


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['ip_address']


admin.site.register(BugReport, BugReportAdmin)
admin.site.register(FileReport, FileReportAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)
admin.site.register(CommandActivity, CommandActivityAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
