from django.urls import path

from . import views

urlpatterns = [
    path("pay/", views.pay_with_esewa, name="pay_with_esewa"),
    path("success/", views.esewa_success, name="esewa_success"),
    path("failure/", views.esewa_failure, name="esewa_failure"),
]