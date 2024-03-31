from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    profile_pic = models.ImageField(null=True,blank=True, upload_to='profile_pics',default='profile_pics/default.jpeg')

    def __str__(self):
        return self.user.username



class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    


class Product(models.Model):

    CATEOGORY = ( ('Indoor','Indoor'),('Outdoor','Outdoor') )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True,choices=CATEOGORY)
    description =models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS =( ('Pending','Pending'),('On the Way','On the Way'),('Delivered','Delivered') ) # it is just a tuple of tuples
   
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, choices=STATUS,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    note = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return f"{self.product.name}---(status={self.status})"



