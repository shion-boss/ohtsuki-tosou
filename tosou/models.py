from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.

class customer_voice_model(models.Model):
    #img=CloudinaryField('image',null=True, blank=True)
    img=models.ImageField(null=True, blank=True)
    name=models.CharField(max_length=140,blank=True,null=True)
    voice=models.TextField(max_length=140)

class user_meta(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    img=models.ImageField(null=True, blank=True)
    afi_code=models.IntegerField(default=000000)

    def __str__(self):
        return self.afi_code

class qa_model(models.Model):
    question=models.TextField(max_length=200)
    answer=models.TextField(max_length=200)

    def __str__(self):
        return self.question

class catalog_model(models.Model):
    img=models.ImageField(null=True, blank=True)
    number=models.IntegerField(default=0)
    p=models.TextField(max_length=140)

    def __str__(self):
        return self.number

class message_table_model(models.Model):
    title=models.CharField(max_length=150)

class message_user_model(models.Model):
    title=models.ForeignKey(message_table_model,on_delete=models.CASCADE)
    user=models.ForeignKey(SocialAccount,on_delete=models.CASCADE)
    message=models.TextField(max_length=1000)
