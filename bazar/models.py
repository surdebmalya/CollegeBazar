from django.db import models

from django.db import models

class USERS(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    blacklsiornot = models.CharField(max_length=1) # 0 or 1

class ITEMS(models.Model):
    imageURL=models.CharField(max_length=500, null=True)
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=10)
    description=models.CharField(max_length=10000)
    category=models.CharField(max_length=1000)
    userid=models.CharField(max_length=5000)
    status=models.CharField(max_length=1) # 0 or 1

class USER_WISHLISTS(models.Model):
    userid=models.CharField(max_length=5000)
    itemid=models.CharField(max_length=5000)

class CHATROOMS(models.Model):
    roomid = models.CharField(max_length=5000)
    
class MESSAGES(models.Model):
    room= models.CharField(max_length=5000)
    value= models.CharField(max_length=10000)
    user=models.CharField(max_length=5000)
