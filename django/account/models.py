from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    tot_interview = models.IntegerField(default=0, null=True)
    late = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    no_show = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(user=instance)
    instance.profile.save()
