from django.db import transaction

from billing.models import (
    LedgerEntry,
    LedgerEntryType,
    LedgerTransactionType,
    Payment,
)


@transaction.atomic
def create_payment_ledger_entry(
    *,
    payment: Payment,
):
    return LedgerEntry.objects.create(
        student=payment.invoice.student,
        payment=payment,
        entry_type=LedgerEntryType.CREDIT,
        transaction_type=LedgerTransactionType.PAYMENT,
        amount=payment.amount,
    )