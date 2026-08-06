import strawberry
import strawberry_django

from billing.models import LedgerEntry


@strawberry_django.type(LedgerEntry)
class LedgerEntryType:
    id: strawberry.auto
    student: strawberry.auto
    invoice: strawberry.auto
    payment: strawberry.auto
    discount: strawberry.auto
    student_credit: strawberry.auto
    entry_type: strawberry.auto
    transaction_type: strawberry.auto
    amount: strawberry.auto
    notes: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto