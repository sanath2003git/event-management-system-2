from django.contrib import admin
from .models import Event, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_at', 'end_at', 'location', 'created_by')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date', 'created_by')
    ordering = ('date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'booked_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('booked_at',)
    ordering = ('-booked_at',)
