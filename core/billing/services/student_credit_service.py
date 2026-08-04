from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from billing.models import (
    Invoice,
    LedgerEntry,
    LedgerEntryType,
    LedgerTransactionType,
    Payment,
    PaymentStatus,
    StudentCredit,
    StudentCreditReason,
)


@transaction.atomic
def create_student_credit(
    *,
    amount: Decimal,
    reason: StudentCreditReason,
    payment: Payment | None = None,
    invoice: Invoice | None = None,
    notes: str = "",
) -> StudentCredit:

    # Validate amount
    if amount <= Decimal("0.00"):
        raise ValidationError({
            "amount": (
                "Credit amount must be greater than zero."
            )
        })

    # Validate references
    if (payment is None) == (invoice is None):
        raise ValidationError(
            "Provide exactly one of payment or invoice."
        )

    # Validate overpayment credit
    if reason == StudentCreditReason.OVERPAYMENT:

        if payment is None:
            raise ValidationError({
                "payment": (
                    "Overpayment credit must reference "
                    "a payment."
                )
            })

        if payment.status != PaymentStatus.SUCCESSFUL:
            raise ValidationError({
                "payment": (
                    "Only successful payments can "
                    "generate student credit."
                )
            })

        if StudentCredit.objects.filter(
            payment=payment,
            reason=StudentCreditReason.OVERPAYMENT,
        ).exists():
            raise ValidationError({
                "payment": (
                    "An overpayment credit already "
                    "exists for this payment."
                )
            })

        student = payment.invoice.student

    # Validate refund credit
    elif reason == StudentCreditReason.REFUND:

        if invoice is None:
            raise ValidationError({
                "invoice": (
                    "Refund credit must reference "
                    "an invoice."
                )
            })

        student = invoice.student

    else:
        raise ValidationError({
            "reason": (
                "Invalid student credit reason."
            )
        })

    # Generate unique credit note number
    for _ in range(3):

        credit_count = (
            StudentCredit.objects.count() + 1
        )

        credit_note_number = (
            f"CN-{timezone.now().year}-"
            f"{credit_count:06d}"
        )

        try:

            student_credit = StudentCredit.objects.create(
                student=student,
                payment=payment,
                invoice=invoice,
                credit_note_number=credit_note_number,
                reason=reason,
                amount=amount,
                remaining_amount=amount,
                notes=notes,
            )

            break

        except IntegrityError:
            continue

    else:
        raise ValidationError(
            "Unable to generate a unique "
            "credit note number. Please try again."
        )

    # Create ledger entry
    LedgerEntry.objects.create(
        student=student,
        student_credit=student_credit,
        entry_type=LedgerEntryType.CREDIT,
        transaction_type=LedgerTransactionType.CREDIT,
        amount=amount,
    )

    return student_credit