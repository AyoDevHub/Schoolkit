from decimal import Decimal

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from billing.models import Invoice, InvoiceStatus
from billing.exceptions import (
    PaystackInitializationError,
    PaystackVerificationError,
)

def initialize_payment(
    *,
    invoice: Invoice,
    amount: Decimal,
    callback_url: str,
) -> dict:
    """
    Initializes a Paystack transaction and returns the
    authorization URL and reference.
    """

    # Invoice must not already be paid
    if invoice.status == InvoiceStatus.PAID:
        raise ValidationError({
            "invoice": (
                "This invoice has already been fully paid."
            )
        })

    # Student must be active
    if not invoice.student.is_active:
        raise ValidationError({
            "invoice": (
                "Payments cannot be made for inactive students."
            )
        })

    # Amount must be greater than zero
    if amount <= Decimal("0.00"):
        raise ValidationError({
            "amount": (
                "Payment amount must be greater than zero."
            )
        })

    # Outstanding balance
    outstanding_balance = (
        invoice.total_amount
        - total_paid
    )

    if amount > outstanding_balance:
        raise ValidationError({
            "amount": (
                "Payment amount cannot exceed the outstanding balance."
            )
        })

    headers = {
        "Authorization": (
            f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "email": invoice.student.user.email,
        "amount": int(amount * 100),
        "callback_url": callback_url,
        "metadata": {
            "invoice_id": str(invoice.id),
            "student_id": str(invoice.student.id),
        },
    }

    response = requests.post(
        settings.PAYSTACK_INITIALIZE_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    data = response.json()

    if (
        response.status_code != 200
        or not data.get("status")
    ):
        raise PaystackInitializationError(
            data.get(
                "message",
                "Unable to initialize payment.",
            )
            )


    return data["data"]



def verify_transaction(
    *,
    reference: str,
)-> dict:
    """
    Verify a Paystack transaction using its reference.

    Returns the verified transaction data.
    """

    if not reference:
        raise ValidationError({
            "reference": (
                "Payment reference is required."
            )
        })

    headers = {
        "Authorization": (
            f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        )
    }

    response = requests.get(
        f"{settings.PAYSTACK_VERIFY_URL}{reference}",
        headers=headers,
        timeout=30,
    )

    data = response.json()

    if (
        response.status_code != 200
        or not data.get("status")
    ):
        raise PaystackVerificationError(
            data.get(
                "message",
                "Unable to verify transaction.",
            )
        )

    transaction = data["data"]

    if transaction["status"] != "success":
        raise PaystackVerificationError("Payment was not successful.")

    return transaction