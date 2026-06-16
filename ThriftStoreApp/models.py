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
        upload_to='products/', 
        null=True, 
        blank=True
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
    
class CartDb(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDb,on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.DecimalField(default=1,max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class AddressDb(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    house_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class OrderDb(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_id = models.CharField(max_length=200)
    payment_status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(OrderDb,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(ProductDb,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.product.product_name