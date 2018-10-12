from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.db import models
from django.forms import TextInput, Textarea

from .models import Category, Task

admin.site.site_header = 'Meeting | Admin'


class AdminMixin(object):
    list_per_page = 20
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '30'})
        },
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 30})
        }
    }


@admin.register(Category)
class CategoryAdmin(AdminMixin, admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_editable = ('name',)
    readonly_fields = ('user',)
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('user', 'name')}),
    )


@admin.register(Task)
class TaskAdmin(AdminMixin, admin.ModelAdmin):
    actions = ['action_make_not_started', 'action_make_not_open', 'action_make_not_closed', 'action_make_not_cancelled']
    autocomplete_fields = ('category',)
    list_display = ('st', 'descriptions', 'status', 'category', 'owner', 'begin_date', 'end_date', 'progress',)
    list_editable = ('status', 'progress',)
    list_display_links = ('descriptions',)
    readonly_fields = ('user',)
    list_filter = ('status', 'user', 'category',)
    search_fields = ['description', 'status', 'category__name', 'user__username', 'progress']
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Required', {'fields': ('category', 'status', 'description')}),
        ('Optional', {'fields': ('begin', 'end', 'progress')}),
    )

    def save_model(self, request, obj: Task, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def action_make_not_started(self, request, queryset):
        queryset.update(status=Task.NOT_STARTED)

    def action_make_not_open(self, request, queryset):
        queryset.update(status=Task.OPEN)

    def action_make_not_closed(self, request, queryset):
        queryset.update(status=Task.CLOSED)

    def action_make_not_cancelled(self, request, queryset):
        queryset.update(status=Task.CANCELLED)

    action_make_not_started.short_description = "Mark selected tasks as not started"
    action_make_not_open.short_description = "Mark selected tasks as open"
    action_make_not_closed.short_description = "Mark selected tasks as closed"
    action_make_not_cancelled.short_description = "Mark selected tasks as cancelled"

    action_make_not_started.allowed_permissions = ('change_status',)
    action_make_not_open.allowed_permissions = ('change_status',)
    action_make_not_closed.allowed_permissions = ('change_status',)
    action_make_not_cancelled.allowed_permissions = ('change_status',)

    def has_change_status_permission(self, request):
        """Does the user have the change status permission?"""
        opts = self.opts
        codename = get_permission_codename('change_status', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))
