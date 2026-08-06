from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from django.db import transaction
from django.core.exceptions import ValidationError

from billing.exceptions import (
    PaymentProcessingError,
)
from billing.models import (
    Invoice,
    Payment,
    InvoiceStatus,
    PaymentMethod,
    PaymentStatus,
    StudentCreditReason,
)
from billing.services.paystack_gateway_services import (
    verify_transaction,
)
from billing.services.receipt_service import (
    create_receipt,
)
from billing.services.reconciliation_service import (
    reconcile_invoice,
)
from billing.services.student_credit_service import (
    create_student_credit,
)
from billing.services.ledger_entry_services import (
    create_payment_ledger_entry,
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
        status=PaymentStatus.SUCCESSFUL,
    )

    payment.full_clean()
    payment.save()

    # Reconcile payment
    reconcile_invoice(
        invoice=invoice,
    )

    create_receipt(
        payment=payment,
    )

    create_payment_ledger_entry(
        payment=payment,
    )

    total_paid = (
        invoice.payments.filter(
            status=PaymentStatus.SUCCESSFUL,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

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

    return payment




@transaction.atomic
def process_verified_payment(
    *,
    reference: str,
):
    transaction_data = verify_transaction(
        reference=reference,
    )

    if Payment.objects.filter(
        reference=reference,
    ).exists():
        raise ValidationError({
            "reference": (
                "This payment has already been processed."
            )
        })

    metadata = transaction_data.get("metadata", {})

    invoice_id = metadata.get(
        "invoice_id",
    )

    if not invoice_id:
        raise ValidationError({
            "invoice": (
                "Invoice ID is missing from the payment metadata."
            )
        })

    try:
        invoice = Invoice.objects.get(
            id=invoice_id,
        )
    except Invoice.DoesNotExist:
        raise ValidationError({
            "invoice": (
                "Invoice does not exist."
            )
        })

    received_amount = (
        Decimal(transaction_data["amount"])
        / Decimal("100")
    )
    
    total_paid = (
        invoice.payments.filter(
            status=PaymentStatus.SUCCESSFUL,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    outstanding_balance = (
        invoice.total_amount
        - total_paid
    )

    if received_amount <= Decimal("0.00"):
        raise PaymentProcessingError(
            "Verified payment amount must be greater than zero."
        )

    if received_amount > outstanding_balance:
        raise PaymentProcessingError(
            "Verified payment exceeds the outstanding balance."
        )

    customer_email = (
        transaction_data
        .get("customer", {})
        .get("email")
    )

    if not customer_email:
        raise PaymentProcessingError(
            "Customer email is missing from the payment data."
        )

    if (
        customer_email.lower()
        != invoice.student.user.email.lower()
    ):
        raise PaymentProcessingError(
            "Payment customer does not match invoice owner."
        )

    if transaction_data["currency"] != "NGN":
        raise PaymentProcessingError(
            "Unsupported payment currency."
        )

    if invoice.status == InvoiceStatus.PAID:
        raise PaymentProcessingError(
            "Invoice has already been paid."
        )

    payment_date = parse_datetime(
        transaction_data["paid_at"],
    )

    if payment_date is None:
        raise PaymentProcessingError(
            "Invalid payment date received."
        )

    payment = Payment(
        invoice=invoice,
        amount=received_amount,
        payment_method=PaymentMethod.ONLINE,
        status=PaymentStatus.SUCCESSFUL,
        reference=reference,
        payment_date=payment_date,
    )

    payment.full_clean()
    payment.save()

    reconcile_invoice(
        invoice=invoice,
    )

    create_receipt(
        payment=payment,
    )

    create_payment_ledger_entry(
        payment=payment,
    )

    total_paid = (
        invoice.payments.filter(
            status=PaymentStatus.SUCCESSFUL,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    overpayment = (
        total_paid
        - invoice.total_amount
    )

    if overpayment > Decimal("0.00"):
        create_student_credit(
            amount=overpayment,
            reason=StudentCreditReason.OVERPAYMENT,
            payment=payment,
        )

    return payment