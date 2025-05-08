from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# from django.db import models

class pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    type = models.CharField(max_length= 40)
    breed = models.CharField(max_length=40)
    price = models.IntegerField()
    gender=models.CharField(max_length=6,default='')
    description=models.CharField(max_length=100,default='')
    petimage=models.ImageField(upload_to="image",default='')

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    petid=models.ForeignKey(pet,on_delete=models.CASCADE,db_column='petid')
    quantity=models.IntegerField(default=1)

class myOrder(models.Model):
    orderid=models.CharField(max_length=49)
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    petid=models.ForeignKey(pet,on_delete=models.CASCADE,db_column='petid')
    quantity=models.IntegerField()