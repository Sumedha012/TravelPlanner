from django.contrib import admin
from .models import Destination, UserPreference

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'budget', 'image_url')
    search_fields = ('name', 'location')
    list_filter = ('type', 'budget')

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('destination_type', 'budget', 'start_date', 'end_date')
    search_fields = ('destination_type', 'budget')
