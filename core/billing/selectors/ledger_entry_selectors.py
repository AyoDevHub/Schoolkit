from django.db.models import Sum
from decimal import Decimal

from billing.models import (
    LedgerEntry,
    LedgerEntryType,
)


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_ledger_entry_by_id(
    ledger_entry_id: str,
) -> LedgerEntry:
    return LedgerEntry.objects.get(
        id=ledger_entry_id,
    )


def list_ledger_entries(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        student__school_id=school_id,
    )[offset:offset + limit]


def list_ledger_entries_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        student_id=student_id,
    )[offset:offset + limit]


def list_ledger_entries_by_invoice(
    invoice_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        invoice_id=invoice_id,
    )[offset:offset + limit]


def list_ledger_entries_by_payment(
    payment_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        payment_id=payment_id,
    )[offset:offset + limit]


def list_ledger_entries_by_discount(
    discount_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        discount_id=discount_id,
    )[offset:offset + limit]


def list_ledger_entries_by_student_credit(
    student_credit_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        student_credit_id=student_credit_id,
    )[offset:offset + limit]


def list_ledger_entries_by_transaction_type(
    school_id: str,
    transaction_type: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        student__school_id=school_id,
        transaction_type=transaction_type,
    )[offset:offset + limit]


def list_ledger_entries_by_entry_type(
    school_id: str,
    entry_type: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return LedgerEntry.objects.filter(
        student__school_id=school_id,
        entry_type=entry_type,
    )[offset:offset + limit]


def get_student_balance(
    student_id: str,
) -> Decimal:
    total_debits = (
        LedgerEntry.objects.filter(
            student_id=student_id,
            entry_type=LedgerEntryType.DEBIT,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    total_credits = (
        LedgerEntry.objects.filter(
            student_id=student_id,
            entry_type=LedgerEntryType.CREDIT,
        ).aggregate(
            total=Sum("amount"),
        )["total"]
        or Decimal("0.00")
    )

    return total_debits - total_credits