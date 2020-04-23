from django.contrib import admin
from .models import *

class BudgetAdmin(admin.ModelAdmin):
    search_fields = ['name']

    class Meta:
        model = Budget

class MonthlyBudgetAdmin(admin.ModelAdmin):
    search_fields = ['month', 'planned']
    list_display = ("budget", "month","planned", "actual",)

    class Meta:
        model = MonthlyBudget
    
admin.site.register(Budget, BudgetAdmin)
admin.site.register(MonthlyBudget, MonthlyBudgetAdmin)
