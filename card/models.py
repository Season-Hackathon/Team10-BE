from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings



class Card(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=False, on_delete=models.CASCADE)
    classname = models.CharField(max_length=10,blank=False,null=True)
    userImage = models.ImageField(blank=True, null=True, upload_to="ProfileImage")
class Tag(models.Model):
    card = models.ForeignKey(Card, related_name='tags',on_delete=models.CASCADE)
    tagname = models.CharField(max_length=20,blank=False,default='')
    tagcontent = models.CharField(max_length=50,blank=False,default='')