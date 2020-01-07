from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Cached_Matches(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    matches = models.CharField(max_length=1510, blank=True, null=True)

class Recent_Matches(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    matches = models.CharField(max_length=1510, blank=True, null=True)

class Cached_List_Matches(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    matches = models.CharField(max_length=1510, blank=True, null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Cached_Matches.objects.create(user=instance)
        Recent_Matches.objects.create(user=instance)
        Cached_List_Matches(user=instance)
    instance.profile.save()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     