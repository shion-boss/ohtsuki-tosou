from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import cloudinary
from cloudinary.models import CloudinaryField
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your models here.

class customer_voice_model(models.Model):
    image=CloudinaryField('image',default='https://res.cloudinary.com/hlbrfvwak/image/upload/v1592409791/vaqfgeeaghdbgjcsghg1.jpg',blank=True,null=True)
    #img=models.ImageField(null=True, blank=True)
    name=models.CharField(max_length=140,blank=True,null=True)
    voice=models.TextField(max_length=140)

class c_v_model(models.Model):
    pic=models.CharField(max_length=500,blank=True,null=True,default='https://res.cloudinary.com/hlbrfvwak/image/upload/v1592166538/gpm3ei8ydcd11j6u4x8z.png')
    voice=models.TextField(max_length=140)

class user_meta(models.Model):
    top=models.CharField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=500,blank=True,null=True)
    afi_code=models.CharField(max_length=6,blank=True,null=True)
    uid=models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return self.afi_code

class qa_model(models.Model):
    question=models.TextField(max_length=200)
    answer=models.TextField(max_length=200)

    def __str__(self):
        return self.question

class catalog_model(models.Model):
    image=CloudinaryField('image',default='https://res.cloudinary.com/hlbrfvwak/image/upload/v1592409791/vaqfgeeaghdbgjcsghg1.jpg',blank=True,null=True)
    #img=models.ImageField(null=True, blank=True)
    number=models.IntegerField(default=0)
    p=models.TextField(max_length=140)

    def __str__(self):
        return self.number

class account_meta(models.Model):
    account=models.ForeignKey(SocialAccount,on_delete=models.CASCADE)
    afi_code=models.IntegerField(default=000000)

    def __str__(self):
        return self.afi_code


class message_table_model(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self):
        return self.title

class message_user_model(models.Model):
    title=models.ForeignKey(message_table_model,on_delete=models.CASCADE)
    uid=models.CharField(max_length=500,blank=True,null=True,default='technext')
    message=models.TextField(max_length=1000)

    def __str__(self):
        return self.message

class code_model(models.Model):
    option=models.IntegerField(default=0)
    num=models.IntegerField(default=10000)
