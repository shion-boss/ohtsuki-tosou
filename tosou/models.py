from django.db import models
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.

class customer_voice_model(models.Model):
    #img=CloudinaryField('image',null=True, blank=True)
    img=models.ImageField(null=True, blank=True)
    voice=models.TextField(max_length=140)

class user_meta(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.ImageField(null=True, blank=True)
    afi_code=models.IntegerField(default=000000)

class qa_model(models.Model):
    question=models.TextField(max_length=200)
    answer=models.TextField(max_length=200)

class catalog_model(models.Model):
    img=models.ImageField(null=True, blank=True)
    number=models.IntegerField(default=0)
    p=models.TextField(max_length=140)
