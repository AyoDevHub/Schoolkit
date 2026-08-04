import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class StudentCreditReason(models.TextChoices):
    OVERPAYMENT = "overpayment", "Overpayment"
    REFUND = "refund", "Refund"


class StudentCredit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.PROTECT,
        related_name="student_credits",
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.PROTECT,
        related_name="student_credits",
        null=True,
        blank=True,
    )

    payment = models.ForeignKey(
        "billing.Payment",
        on_delete=models.PROTECT,
        related_name="student_credits",
        null=True,
        blank=True,
    )

    credit_note_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    reason = models.CharField(
        max_length=20,
        choices=StudentCreditReason.choices,
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

    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.00"),
            ),
        ],
    )

    notes = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_student_credits"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return (
            f"{self.credit_note_number} - "
            f"{self.student.full_name}"
        )

    def clean(self):
        if self.remaining_amount > self.amount:
            raise ValidationError({
                "remaining_amount": (
                    "Remaining amount cannot exceed "
                    "the original credit amount."
                )
            })

        references = [
            self.invoice,
            self.payment,
        ]

        provided_references = sum(
            reference is not None
            for reference in references
        )

        if provided_references != 1:
            raise ValidationError(
                "A student credit must reference exactly "
                "one invoice or payment."
            )

        if (
            self.reason == StudentCreditReason.OVERPAYMENT
            and self.payment is None
        ):
            raise ValidationError({
                "payment": (
                    "An overpayment credit must reference "
                    "the payment that created it."
                )
            })

        if (
            self.reason == StudentCreditReason.REFUND
            and self.invoice is None
        ):
            raise ValidationError({
                "invoice": (
                    "A refund credit must reference "
                    "the invoice that created it."
                )
            })

    def save(
        self,
        *args,
        **kwargs,
    ):
        self.full_clean()

        self.is_active = (
            self.remaining_amount > Decimal("0.00")
        )

        super().save(
            *args,
            **kwargs,
        )