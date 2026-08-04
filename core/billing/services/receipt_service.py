from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from billing.models import (
    Payment,
    PaymentStatus,
    Receipt,
)


@transaction.atomic
def create_receipt(
    *,
    payment: Payment,
    notes: str = "",
) -> Receipt:

    # Payment must be successful
    if payment.status != PaymentStatus.SUCCESSFUL:
        raise ValidationError({
            "payment": (
                "A receipt can only be generated "
                "for a successful payment."
            )
        })

    # Prevent duplicate receipts
    if Receipt.objects.filter(
        payment=payment,
    ).exists():
        raise ValidationError({
            "payment": (
                "A receipt has already been "
                "generated for this payment."
            )
        })

    for _ in range(3):

        receipt_count = Receipt.objects.count() + 1

        receipt_number = (
            f"RCT-{timezone.now().year}-{receipt_count:06d}"
        )

        try:
            return Receipt.objects.create(
                payment=payment,
                receipt_number=receipt_number,
                notes=notes,
            )

        except IntegrityError:
            continue

    raise ValidationError(
        "Unable to generate a unique receipt number. "
        "Please try again."
    )