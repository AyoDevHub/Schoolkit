from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from billing.models import (
    InvoiceStatus,
    LedgerEntry,
    LedgerEntryType,
    LedgerTransactionType,
    Payment,
    PaymentStatus,
    Receipt,
    StudentCreditReason,
)
from billing.services.receipt_service import create_receipt
from billing.services.student_credit_service import (
    create_student_credit,
)


@transaction.atomic
def reconcile_payment(
    *,
    payment: Payment,
) -> None:
    # Validate payment status
    if payment.status != PaymentStatus.SUCCESSFUL:
        raise ValidationError({
            "payment": (
                "Only successful payments "
                "can be reconciled."
            )
        })

    invoice = payment.invoice

    # Calculate total successful payments
    total_paid = (
        Payment.objects.filter(
            invoice=invoice,
            status=PaymentStatus.SUCCESSFUL,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    # Update invoice status
    if total_paid == Decimal("0.00"):
        invoice.status = InvoiceStatus.UNPAID

    elif total_paid < invoice.total_amount:
        invoice.status = InvoiceStatus.PARTIALLY_PAID

    else:
        invoice.status = InvoiceStatus.PAID

    invoice.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    # Create ledger entry for the payment
    if not LedgerEntry.objects.filter(
        payment=payment,
        transaction_type=LedgerTransactionType.PAYMENT,
    ).exists():

        LedgerEntry.objects.create(
            student=invoice.student,
            payment=payment,
            entry_type=LedgerEntryType.CREDIT,
            transaction_type=LedgerTransactionType.PAYMENT,
            amount=payment.amount,
        )

    # Generate receipt
    if not Receipt.objects.filter(
        payment=payment,
    ).exists():
        create_receipt(
            payment=payment,
        )

    # Create student credit for overpayment
    overpayment = (
        total_paid
        - invoice.total_amount
    )

    if overpayment > Decimal("0.00"):

        create_student_credit(
            payment=payment,
            amount=overpayment,
            reason=StudentCreditReason.OVERPAYMENT,
        )