import strawberry
import strawberry_django

from billing.models import Payment


@strawberry.type
class PaystackInitializationResponse:
    authorization_url: str
    access_code: str
    reference: str


@strawberry_django.type(Payment)
class PaymentType:
    id: strawberry.auto
    invoice: strawberry.auto
    amount: strawberry.auto
    payment_method: strawberry.auto
    status: strawberry.auto
    reference: strawberry.auto
    payment_date: strawberry.auto
    notes: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto