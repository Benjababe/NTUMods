from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'lat', 'long']
