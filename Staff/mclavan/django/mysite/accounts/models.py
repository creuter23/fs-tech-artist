from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Students(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # This should be an enum.
    class_id = models.CharField(max_length=7)
    # email = models.EmailField()

    def __unicode__(self):
        return '%s %s' %(self.first_name, self.last_name)

