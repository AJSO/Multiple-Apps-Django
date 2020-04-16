from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    username = models.CharField(max_length=40)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=35)
    about = models.TextField()

    
    def create_user_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(user=kwargs['instance'])
           
    post_save.connect(create_user_profile, sender=User)

class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='profile_pics', blank=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

    # overriding the save method
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300) #tuple
    #         img.thumbnail(output_size)
    #         img.save(self.image.path) 

    
    def create_user_profile_pic(sender, **kwargs):
        if kwargs['created']:
            user_profile = ProfilePic.objects.create(user=kwargs['instance'])
           
    post_save.connect(create_user_profile_pic, sender=User)     
