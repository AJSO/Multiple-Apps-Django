from django.contrib import admin

from .models import *

class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['title', 'category']
    list_display = ("title", "category","created", "due_date",)

    class Meta:
        model = Task

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
        
    class Meta: model = Category

admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
