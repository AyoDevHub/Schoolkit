import strawberry
import strawberry_django

from billing.models import Discount


@strawberry_django.type(Discount)
class DiscountType:
    id: strawberry.auto
    school: strawberry.auto
    student: strawberry.auto
    academic_session: strawberry.auto
    academic_term: strawberry.auto
    discount_type: strawberry.auto
    value_type: strawberry.auto
    value: strawberry.auto
    reason: strawberry.auto
    approved_by: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto