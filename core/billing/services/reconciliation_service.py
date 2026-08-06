from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from billing.models import (
    InvoiceStatus,
    Invoice,
)


@transaction.atomic
def reconcile_invoice(
    *,
    invoice: Invoice,
):

    total_paid = (
        invoice.payments.filter(
            status=PaymentStatus.SUCCESSFUL,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    if total_paid <= Decimal("0.00"):
        invoice.status = InvoiceStatus.UNPAID

    elif total_paid < invoice.total_amount:
        invoice.status = InvoiceStatus.PARTIALLY_PAID

    else:
        # Covers both fully paid and overpaid invoices.
        invoice.status = InvoiceStatus.PAID

    invoice.save(
        update_fields=[
            "status",
        ]
    )

    return invoice