from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OfferProduct)
admin.site.register(Category)
admin.site.register(SubCategory)

class ProductAdminImage(admin.TabularInline):
    model=ProductImage
    extra=2

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','category']
    inlines=[ProductAdminImage]

 
    

