import uuid as uuid_lib

from django.conf import settings
from django.db import models


class Transaction(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_COMPLETE = "COMPLETE"
    STATUS_FAILED = "FAILED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETE, "Complete"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    # Generated automatically when the row is created — this is what we send
    # to eSewa and what we look the transaction up by on the callback.
    transaction_uuid = models.CharField(
        max_length=100, unique=True, default=uuid_lib.uuid4, editable=False
    )
    # eSewa's own reference code — only known after payment, filled in on success.
    transaction_code = models.CharField(max_length=200, blank=True)
    product_code = models.CharField(max_length=200)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_uuid} — {self.status} — Rs.{self.total_amount}"


class Order(models.Model):
    """
    Created exactly once, at the moment a Transaction is confirmed COMPLETE.
    The OneToOne link to Transaction is what makes this safe to create
    with get_or_create() even if the success callback somehow runs twice
    (bookmarked URL, double-click, browser back button) — the second call
    just finds the existing Order instead of making a duplicate.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="order",
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} — {self.user} — Rs.{self.total_amount}"


class OrderItem(models.Model):
    """
    A snapshot of one cart line at the moment of purchase. We store the
    product's name/price/image directly here instead of just a foreign key
    to Product — that way, if the product's price changes or it gets
    deleted later, this order still shows exactly what the customer
    actually paid for.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.URLField(blank=True)

    def __str__(self):
        return f"{self.quantity} × {self.name}"

    @property
    def line_total(self):
        return self.price * self.quantity