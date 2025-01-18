from django.contrib import admin

# Register your models here.
from .models import Report
from import_export.admin import ImportExportModelAdmin

@admin.register(Report)
class YourModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id', 'description', 'solutions')
    
