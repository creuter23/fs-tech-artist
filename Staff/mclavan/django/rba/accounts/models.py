from django.db import models

# Create your models here.
class People(models.Model):
    nick_name = models.CharField(max_length=30)
    class_id = models.CharField(max_length=7)
    email = models.EmailField()
    disc_types = (('ANIM', 'Animation'), ('MOD', 'Modeling'), ('SAL', 'Shading & Lighting'), ('COMP', 'Compositing'),
        ('RIG', 'Rigging'), ('VFX', 'Visual Effects'))
    disc = models.CharField(max_length=5, choices=disc_types)

    
    
    