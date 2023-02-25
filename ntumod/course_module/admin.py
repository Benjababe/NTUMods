from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'module']
    search_fields = ['course', 'module']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'desc', 'grading', 'credits']
    search_fields = ['code', 'name', 'desc', 'grading', 'credits']


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'sub_code', 'year', 'name', 'type']
    search_fields = ['code', 'sub_code', 'year', 'name', 'type']
