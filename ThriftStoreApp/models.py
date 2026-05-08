from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    USER = (
        ('admin','Admin'),
        ('seller','Seller'),
        ('buyer','Buyer'),
    )
    role = models.CharField(choices=USER,max_length=10,default='buyer')
    user_image=models.ImageField(upload_to='user_images/',null=True,blank=True)

class CategoryDb(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(
        upload_to='category_images/',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.category_name
    
class ProductDb(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_category = models.ForeignKey(
        CategoryDb,
        on_delete=models.CASCADE
    )
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(
        upload_to='product_images/'
    )
    product_seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product_name