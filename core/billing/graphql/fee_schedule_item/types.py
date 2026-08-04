import strawberry
import strawberry_django

from billing.models import FeeScheduleItem


@strawberry_django.type(FeeScheduleItem)
class FeeScheduleItemType:
    id: strawberry.auto
    fee_schedule: strawberry.auto
    fee_item: strawberry.auto
    amount: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto