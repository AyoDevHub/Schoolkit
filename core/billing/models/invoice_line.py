import uuid
from decimal import Decimal

from django.db import models


class InvoiceLine(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.CASCADE,
        related_name="invoice_lines",
    )

    fee_item = models.ForeignKey(
        "billing.FeeItem",
        on_delete=models.PROTECT,
        related_name="invoice_lines",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_invoice_lines"

        ordering = [
            "created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "invoice",
                    "fee_item",
                ],
                name="unique_fee_item_per_invoice",
            ),
        ]

    def __str__(self):
        return (
            f"{self.invoice.invoice_number} - "
            f"{self.fee_item.name}"
        )