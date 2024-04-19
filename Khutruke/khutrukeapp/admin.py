from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'acquired')  # Display these fields in the admin list view
    list_filter = ('acquired',)  # Add a filter for the 'acquired' field
