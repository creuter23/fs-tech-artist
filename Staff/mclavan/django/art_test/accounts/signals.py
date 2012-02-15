from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.contrib.auth.models import User
#from models import UserProfile
import art_test
from django.db import models

def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = art_test.accounts.models.UserProfile(user=user, disc_id=1,
                                                       student_id=555553,
                                                       user_level='s',
                                                       class_id='PCC'
                                                        )
        profile.save()

post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")