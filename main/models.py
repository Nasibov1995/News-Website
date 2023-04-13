from django.db import models



class Newsdata(models.Model):
    link= models.CharField(max_length=1000)
    basliq= models.CharField(max_length=1000)
    foto= models.CharField(max_length=1000)
    metn= models.CharField(max_length=1000)
    kateqoriya = models.CharField(max_length=1000)
    temp = models.CharField(max_length=100)
    tarix= models.CharField(max_length=1000)

    
    def __str__(self):
        return self.basliq
    def get_absolute_url(self):
        return f'/'

class Contactus(models.Model):
    message= models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    subject= models.CharField(max_length=100)
    
    def __str__(self):
        return self.message
    def get_absolute_url(self):
        return f'/'

class Comments(models.Model):
    comment= models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    website= models.CharField(max_length=100)
    meqale_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.comment
    def get_absolute_url(self):
        return f'/'