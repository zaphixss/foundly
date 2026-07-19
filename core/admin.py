from django.contrib import admin
from .models import Report, Category

# Register your models here.

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'report_type', 'status', 'created_at')

admin.site.register(Category)