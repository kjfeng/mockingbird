from django.contrib import admin
from onboard.models import Profile
from .models import Cached_Matches, Recent_Matches

# # Register your models here.
admin.site.register(Cached_Matches)
admin.site.register(Recent_Matches)
