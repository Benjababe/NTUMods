from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['type', 'group', 'day', 'time_start', 'time_end', 'venue', 'module']
    search_fields = ['type', 'group', 'day', 'time_start', 'time_end', 'venue', 'module']
