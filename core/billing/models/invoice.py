import uuid
from decimal import Decimal
from django.db.models import Sum
from django.db import models

from billing.models.payment import PaymentStatus


class InvoiceStatus(models.TextChoices):
    UNPAID = "unpaid", "Unpaid"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"


class Invoice(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    academic_session = models.ForeignKey(
        "schools.AcademicSession",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    academic_term = models.ForeignKey(
        "schools.AcademicTerm",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    fee_schedule = models.ForeignKey(
        "billing.FeeSchedule",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.UNPAID,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    discount_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
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
        db_table = "billing_invoices"

        ordering = [
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_session",
                    "academic_term",
                ],
                name="unique_invoice_per_student_session_term",
            ),
        ]

    def __str__(self):
        return self.invoice_number