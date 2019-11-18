from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


INDUSTRY_CHOICES = [('Technology', 'Technology'),
                    ('Finance', 'Finance'),
                    ('Consulting', 'Consulting')]

FRESHMAN = 'Freshman'
SOPHOMORE = 'Sophomore'
JUNIOR = 'Junior'
SENIOR = 'Senior'
GRADUATE_STUDENT = 'Graduate Student'
POST_DOC = 'Postdoc'
NA = 'Not in School'
YEAR_IN_SCHOOL_CHOICES = [
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
    (GRADUATE_STUDENT, 'Graduate Student'),
    (POST_DOC, 'Postdoc'),
    (NA, 'Not in School'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.TextField(max_length=100, blank=False)
    email_confirmed = models.BooleanField(default=False)
    onboard_confirmed = models.BooleanField(default=False)
    # industry
    industry = MultiSelectField(max_length=30, blank=False, choices=INDUSTRY_CHOICES)


    #industry = models.CharField(max_length=30, blank=False, choices=INDUSTRY_CHOICES)

    role = models.CharField(max_length=30, blank=False, default="Unknown")
    # major
    major = models.CharField(max_length=100, blank=False, default="Unknown")

    # years

    year_in_school = models.CharField(
        max_length=20,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default="Unknown",
    )

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
