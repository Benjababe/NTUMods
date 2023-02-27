from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.TeachingStaff)
class TeachingStaffAdmin(admin.ModelAdmin):
    list_display = ['title', 'email']
    search_fields = ['title', 'email', 'tag']
    
@admin.register(models.Appointment)
class StaffAppointmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(models.Interest)
class StaffInterestAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']