from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    disc = models.CharField(null=True, max_length=18)
    classid = models.CharField(max_length=4)
    student_id = models.IntegerField(10)
    comments = models.CharField(null=True, max_length=255)

    def __unicode__(self):
        return '%s: %s %s' %(self.name, self.user_name, self.email)
 
# Username: mclavan_hsdb dbPassword = FS!@#$% student table
class Art_Test(models.Model):
    # Setting up enum type
    status_types = ((u'p', u'passed'), (u'1', u'1'), (u'2', u'2'), (u'3', u'3'), (u'e', u'except'))
    asset_types = ((u'y', u'yes'), (u'n', u'no'))
    asses_types = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    AT_status = models.CharField(max_length=5, choices=status_types)
    asset_status = models.CharField(max_length=2, choices=asset_types)
    assesment = models.CharField(max_length=6, choices=asses_types)
    student = models.ForeignKey(Student)
    art_director = models.CharField(max_length=50)
    AD_Email = models.EmailField(max_length=100)
    






class Disc(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey('users.Category')

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_blog_post', None, { 'slug': self.slug })

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('view_disc_category', None, { 'slug': self.slug })

