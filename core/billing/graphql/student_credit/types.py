import strawberry
import strawberry_django

from billing.models import StudentCredit


@strawberry_django.type(StudentCredit)
class StudentCreditType:
    id: strawberry.auto
    student: strawberry.auto
    invoice: strawberry.auto
    payment: strawberry.auto
    credit_note_number: strawberry.auto
    reason: strawberry.auto
    amount: strawberry.auto
    remaining_amount: strawberry.auto
    notes: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto