import strawberry
import strawberry_django

from billing.models import Receipt


@strawberry_django.type(Receipt)
class ReceiptType:
    id: strawberry.auto
    payment: strawberry.auto
    receipt_number: strawberry.auto
    notes: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto