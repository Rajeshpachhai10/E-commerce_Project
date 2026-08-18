from django.urls import path
from .views import *

urlpatterns = [
    path("", index , name="index"),
    path("product_detail/<int:id>", product_detail , name="product_detail")
    
]
