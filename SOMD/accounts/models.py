from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    
    college = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    profile_pic = models.ImageField(upload_to='user_profile/', default='user_profile/usrDefaultImage.png')
    
    intro = models.CharField(max_length=100, blank=True, null=True, default="")
    email = models.CharField(max_length=100, blank=True, null=True)
    #없앨거에요?
    nickname = models.CharField(max_length=10)
    

    def __str__(self):
        return self.user.username