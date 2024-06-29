from django.db import models
import uuid
from  django.conf import settings
from rest_framework.permissions import IsAuthenticated



# Create your models here.

        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description

    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')
    old_price = models.FloatField(blank=True, null=True)
    price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    stock = models.IntegerField(default=6)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:  # If the product already exists (updating)
            try:
                old_product = Product.objects.get(pk=self.pk)
                if old_product.price != self.price:
                    self.old_price = old_product.price
            except Product.DoesNotExist:
                pass  
        
        super(Product, self).save(*args, **kwargs)

