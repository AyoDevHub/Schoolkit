import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class LedgerEntryType(models.TextChoices):
    DEBIT = "debit", "Debit"
    CREDIT = "credit", "Credit"


class LedgerTransactionType(models.TextChoices):
    INVOICE = "invoice", "Invoice"
    PAYMENT = "payment", "Payment"
    DISCOUNT = "discount", "Discount"
    CREDIT = "credit", "Credit"
    ADJUSTMENT = "adjustment", "Adjustment"


class LedgerEntry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.PROTECT,
        related_name="ledger_entries",
    )

    invoice = models.ForeignKey(
        "billing.Invoice",
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        null=True,
        blank=True,
    )

    payment = models.ForeignKey(
        "billing.Payment",
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        null=True,
        blank=True,
    )

    discount = models.ForeignKey(
        "billing.Discount",
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        null=True,
        blank=True,
    )

    student_credit = models.ForeignKey(
        "billing.StudentCredit",
        on_delete=models.PROTECT,
        related_name="ledger_entries",
        null=True,
        blank=True,
    )

    entry_type = models.CharField(
        max_length=10,
        choices=LedgerEntryType.choices,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=LedgerTransactionType.choices,
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
        db_table = "billing_ledger_entries"

        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.transaction_type} - ₦{self.amount}"

    def clean(self):
        references = {
            LedgerTransactionType.INVOICE: self.invoice,
            LedgerTransactionType.PAYMENT: self.payment,
            LedgerTransactionType.CREDIT: self.student_credit,
            LedgerTransactionType.DISCOUNT: self.discount,
        }

        provided_references = [
            reference for reference in references.values() if reference is not None
        ]

        if len(provided_references) != 1:
            raise ValidationError(
                "A ledger entry must reference exactly one of "
                "invoice, payment, discount, or student credit."
            )

        expected_reference = references.get(
            self.transaction_type,
        )

        if self.transaction_type in references and expected_reference is None:
            raise ValidationError(
                {
                    "transaction_type": (
                        f"{self.get_transaction_type_display()} "
                        "entries must reference the corresponding object."
                    )
                }
            )

        if self.transaction_type == LedgerTransactionType.ADJUSTMENT:
            raise ValidationError(
                {"transaction_type": ("Manual adjustments are not supported yet.")}
            )
