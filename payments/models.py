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