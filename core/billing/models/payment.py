import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    CARD = "card", "Card"
    ONLINE = "online", "Online"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESSFUL = "successful", "Successful"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01"),
            ),
        ],
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    payment_date = models.DateTimeField()

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
        db_table = "billing_payments"

        ordering = [
            "-payment_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "reference",
                ],
                condition=models.Q(
                    reference__isnull=False,
                ),
                name="unique_payment_reference",
            ),
        ]

    def __str__(self):
        return (
            f"{self.invoice.invoice_number} - "
            f"₦{self.amount}"
        )