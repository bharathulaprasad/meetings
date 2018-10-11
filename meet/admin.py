from django.contrib import admin

from .models import Category, Task

admin.site.site_header = 'Meeting | Admin'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'st',
        'descriptions',
        'status',
        'category',
        'owner',
        'begin_date',
        'end_date',
        'progress',
    )
    list_editable = (
        'status',
        'progress',
    )
    list_display_links = (
        'descriptions',
    )
    readonly_fields = (
        'user',
    )

    def save_model(self, request, obj: Task, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)
