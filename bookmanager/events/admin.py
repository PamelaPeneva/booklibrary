from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')
    search_fields = ('location', 'start_time', 'title')
    list_filter = ('location', 'start_time')

