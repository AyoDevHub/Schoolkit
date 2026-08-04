from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from billing.models import (
    Invoice,
    InvoiceStatus,
    Payment,
    PaymentMethod,
    PaymentStatus,
)
from billing.services.reconciliation_service import (
    reconcile_payment,
)


@transaction.atomic
def record_offline_payment(
    *,
    invoice: Invoice,
    amount: Decimal,
    payment_method: PaymentMethod,
    payment_date: datetime,
    reference: str = "",
    notes: str = "",
) -> Payment:

    # Invoice must not already be fully paid
    if invoice.status == InvoiceStatus.PAID:
        raise ValidationError({
            "invoice": (
                "This invoice has already been fully paid."
            )
        })

    # Validate amount
    if amount <= Decimal("0.00"):
        raise ValidationError({
            "amount": (
                "Payment amount must be greater than zero."
            )
        })

    # Validate payment date
    if payment_date.date() < invoice.created_at.date():
        raise ValidationError({
            "payment_date": (
                "Payment date cannot be earlier than "
                "the invoice creation date."
            )
        })

    if payment_date > timezone.now():
        raise ValidationError({
            "payment_date": (
                "Payment date cannot be in the future."
            )
        })

    # Validate student status
    if not invoice.student.is_active:
        raise ValidationError({
            "invoice": (
                "Payments cannot be recorded "
                "for inactive students."
            )
        })

    # Validate payment method
    if payment_method not in PaymentMethod.values:
        raise ValidationError({
            "payment_method": (
                "Invalid payment method."
            )
        })

    # Clean reference
    reference = reference.strip()

    # Validate payment reference
    if (
        reference
        and Payment.objects.filter(
            reference=reference,
        ).exists()
    ):
        raise ValidationError({
            "reference": (
                "A payment with this reference "
                "already exists."
            )
        })

    # Create payment
    payment = Payment(
        invoice=invoice,
        amount=amount,
        payment_method=payment_method,
        payment_date=payment_date,
        reference=reference or None,
        notes=notes,
    )

    payment.full_clean()
    payment.save()

    # Mark payment successful
    payment.status = PaymentStatus.SUCCESSFUL

    payment.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    # Reconcile payment
    reconcile_payment(
        payment=payment,
    )

    return payment