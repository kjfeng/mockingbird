from django.contrib import admin
# Register your models here.

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('time_matched',)

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
