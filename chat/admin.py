from django.contrib import admin
from .models import Thread, ChatMessage

# Register your models here.
class ChatMessage(admin.TabularInline):
    model = ChatMessage

# Creates a relationship of ChatMessage to Thread such that
# multiple instances of ChatMessage can be created and managed
# in a Thread instance
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)

