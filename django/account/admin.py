from django.contrib import admin

from .models import Statistics, NotificationItem

# Register your models here.
admin.site.register(Statistics)
admin.site.register(NotificationItem)