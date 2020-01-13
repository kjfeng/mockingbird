from django.contrib import admin
from .models import Cached_Matches, Recent_Matches

# # Register your models here.
admin.site.register(Cached_Matches)
admin.site.register(Recent_Matches)
