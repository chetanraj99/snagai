from django.contrib import admin

# Register your models here.
from .models import Report

@admin.register(Report)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'solutions')
    
