import uuid

from django.db import models


class Receipt(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    payment = models.OneToOneField(
        "billing.Payment",
        on_delete=models.PROTECT,
        related_name="receipt",
    )

    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_receipts"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return self.receipt_number