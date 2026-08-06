import strawberry
import strawberry_django

from billing.models import Invoice


@strawberry_django.type(Invoice)
class InvoiceType:
    id: strawberry.auto
    school: strawberry.auto
    student: strawberry.auto
    academic_session: strawberry.auto
    academic_term: strawberry.auto
    fee_schedule: strawberry.auto
    invoice_number: strawberry.auto
    due_date: strawberry.auto
    status: strawberry.auto
    subtotal: strawberry.auto
    discount_total: strawberry.auto
    total_amount: strawberry.auto
    notes: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto