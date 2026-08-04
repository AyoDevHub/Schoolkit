import strawberry

from billing.graphql.fee_item.types import FeeItemType
from billing.graphql.permissions import CanViewFeeItem
from billing.selectors.fee_item_selectors import (
    get_fee_item_by_id,
    list_active_fee_items,
    list_fee_items,
    list_inactive_fee_items,
)


@strawberry.type
class FeeItemQuery:

    @strawberry.field(
        permission_classes=[CanViewFeeItem]
    )
    def fee_item(
        self,
        fee_item_id: strawberry.ID,
    ) -> FeeItemType | None:
        return get_fee_item_by_id(fee_item_id)


    @strawberry.field(
        permission_classes=[CanViewFeeItem]
    )
    def fee_items(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[FeeItemType]:
        return list_fee_items(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewFeeItem]
    )
    def active_fee_items(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[FeeItemType]:
        return list_active_fee_items(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewFeeItem]
    )
    def inactive_fee_items(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[FeeItemType]:
        return list_inactive_fee_items(
            school_id,
            offset=offset,
            limit=limit,
        )