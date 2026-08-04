import uuid


from django.core.validators import MinValueValidator
from django.db import models


class FeeScheduleItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    fee_schedule = models.ForeignKey(
        "billing.FeeSchedule",
        on_delete=models.CASCADE,
        related_name="fee_schedule_items",
    )

    fee_item = models.ForeignKey(
        "billing.FeeItem",
        on_delete=models.PROTECT,
        related_name="fee_schedule_items",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_fee_schedule_items"

        ordering = [
            "fee_item",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "fee_schedule",
                    "fee_item",
                ],
                name="unique_fee_item_per_fee_schedule",
            ),
        ]

    def __str__(self):
        return (
            f"{self.fee_item} - ₦{self.amount}"
        )

        
