from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from phone_field import PhoneField

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

INDUSTRY_CHOICES = [('None', 'None'),
                    ('Consulting', 'Consulting'),
                    ('Finance', 'Finance'),
                    ('Technology', 'Technology'),
                    ]

ERROR_MESSAGES = {'Dup Industry':'Industry choice 1 and Industry choice 2 must be distinct.',
                  'No Industry 1':'You must make a selection for Industry choice 1.',
                  'Industry Match': 'You do not have a selection for Industry choice 2 so Industry Match must be \'Industry 1\'.'}

INDUSTRY_MATCH_CHOICE = [('Industry 1', 'Industry 1'),
                        ('Industry 2', 'Industry 2'),
                        ('Both', 'Both')]

RANK_CHOICES = [('Industry', 'Industry'),
                  ('Role', 'Role'),
                  ('Year In School', 'Year In School'),
                  ('Similar Interviews', 'Similar # of Interviews'),
                  ('Most Interviews', 'Most # Interviews'),
                  ('Rating', 'Rating')]

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
    email_confirmed = models.BooleanField(default=False)
    onboard_confirmed = models.BooleanField(default=False)
    
    # industry
    industry_choice_1 = models.CharField(max_length=30, blank=False, choices=INDUSTRY_CHOICES, default='None')
    industry_choice_2 = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, default='None')


    role = models.CharField(max_length=30, blank=False, default="Unknown")

    # Match Configuration
    industry_match = models.CharField(max_length=30, blank=False, choices=INDUSTRY_MATCH_CHOICE, default='Industry 1') 
    rank_by = MultiSelectField(max_length=200, blank=False, choices=RANK_CHOICES)

    # major
    major = models.CharField(max_length=100, blank=False, default="Unknown")

    # years
    year_in_school = models.CharField(
        max_length=20,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default="Unknown",
    )

    is_matched = models.BooleanField(default=False)
    has_request = models.BooleanField(default=False)
    match_name = models.CharField(max_length=100, default="None")
    requested_names = models.CharField(max_length=3000, blank=True)

    # is this user  the sender
    is_sender = models.BooleanField(default=False)
    # countdown from time matched
    time_matched = models.DateTimeField(auto_now=True)
    # boolean to say if this is a sender waiting for someone to response to their request
    is_waiting = models.BooleanField(default=False)

    # Contact Information Settings
    receive_email = models.BooleanField(default=True, choices=BOOL_CHOICES)

    # whether or not they are to be matched
    is_idle = models.BooleanField(default=False, choices=BOOL_CHOICES)

    summary = models.CharField(max_length=500, blank=True)

    request_name = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
