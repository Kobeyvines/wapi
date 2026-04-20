from django.contrib import admin
from .models import Event, Category

# This makes your core event data manageable in the dashboard
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer', 'date', 'is_approved')
    list_filter = ('is_approved', 'date', 'categories')
    search_fields = ('name', 'description', 'venue')
    prepopulated_fields = {'slug': ('name',)}