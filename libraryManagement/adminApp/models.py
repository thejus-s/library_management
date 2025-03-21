from django.db import models
from autoslug import AutoSlugField
from userApp.models import *

class category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from= 'name',unique=True)

    def __str__(self):
        return self.name

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='images')
    slug = AutoSlugField(populate_from = 'title',unique=True)
    ISBN = models.CharField(blank=True,null=True)
    category = models.ForeignKey(category,related_name='bookcategory',null=True,blank=True,on_delete=models.CASCADE)
    copies = models.IntegerField()

    def __str__(self):
        return f"{self.title}-({self.category})"
    
class Borrows(models.Model):
    user = models.ForeignKey(User,related_name='user_borrows',on_delete=models.CASCADE)
    book = models.ForeignKey(Books,related_name='book_borrows',on_delete=models.CASCADE)
    borrowed_at = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned_at = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title}-{self.user.fname}"