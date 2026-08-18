from django.db import models
from django.utils import timezone
from datetime import timedelta
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field




# Create your models here.

class OfferProduct(models.Model):
    title=models.CharField(max_length=200)
    desc=models.TextField(max_length=200)
    image=CloudinaryField("offer_images")
    price=models.DecimalField(max_digits=8 ,decimal_places=2)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    desc=CKEditor5Field('Text', config_name='extends')
    image=CloudinaryField("productImages")
    stock_quantity=models.PositiveIntegerField()
    mark_price=models.DecimalField(max_digits=10 ,decimal_places=2)
    discount_percent=models.DecimalField(max_digits=4 ,decimal_places=2)
    price=models.DecimalField(max_digits=10 ,decimal_places=2 ,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        self.price = self.mark_price * (1 - self.discount_percent / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def is_new(self):
        return self.created_at >= timezone.now()-timedelta(days=7)

class ProductImage(models.Model):
    image=CloudinaryField("product_images")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")

    def __str__(self):
        return self.product.name

