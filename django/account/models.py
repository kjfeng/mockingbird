from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


NOT_TYPES = [('MR', 'Match Request'),
            ('CS', 'Complete Survey'),
            ('MC', 'Match Canceled'),
             ('MA', 'Match Accept'),
             ('MD', 'Match Deny/Reject')]

class NotificationItem(models.Model):
    type = models.CharField(
        max_length=100,
        choices=NOT_TYPES,
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_name = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    tot_interview = models.IntegerField(default=0, null=True)
    late = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True)
    no_show = models.IntegerField(default=0, null=True)

    overall_rating = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(user=instance)
    instance.profile.save()
