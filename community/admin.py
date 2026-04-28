from django.contrib import admin
from .models import Follow, Attendance, EventGallery

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'organizer', 'created_at')
    list_filter = ('created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_public', 'joined_at')
    list_filter = ('event', 'is_public')

@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'uploaded_at')