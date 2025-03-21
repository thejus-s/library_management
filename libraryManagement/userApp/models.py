from django.db import models

class User(models.Model):
    role = [
        ('Admin','Admin'),
        ('User','User'),
    ]
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50) 
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=50,choices=role,default='User')
    
    def __str__(self):
        return self.fname