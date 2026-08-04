import strawberry
import strawberry_django

from billing.models import FeeItem


@strawberry_django.type(FeeItem)
class FeeItemType:
    id: strawberry.auto
    school: strawberry.auto
    name: strawberry.auto
    description: strawberry.auto
    is_active: strawberry.auto
    is_recurring: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto