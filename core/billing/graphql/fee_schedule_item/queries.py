import strawberry

from billing.graphql.fee_schedule_item.types import (
    FeeScheduleItemType,
)
from billing.selectors.fee_schedule_item_selectors import (
    get_fee_schedule_item_by_id,
    list_fee_schedule_items_by_fee_schedule,
)
from billing.graphql.permissions import CanViewFeeScheduleItem

@strawberry.type
class FeeScheduleItemQuery:

    @strawberry.field(
            permission_classes=[CanViewFeeScheduleItem]
    )
    def fee_schedule_item(
        self,
        id: strawberry.ID,
    ) -> FeeScheduleItemType | None:
        return get_fee_schedule_item_by_id(id)

    @strawberry.field(
            permission_classes=[CanViewFeeScheduleItem]
    )
    def fee_schedule_items(
        self,
        fee_schedule_id: strawberry.ID,
        offset: int = 0,
        limit: int = 50,
    ) -> list[FeeScheduleItemType]:
        return list_fee_schedule_items_by_fee_schedule(
            fee_schedule_id=fee_schedule_id,
            offset=offset,
            limit=limit,
        )