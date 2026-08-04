import strawberry

from billing.graphql.fee_schedule_item.inputs import (
    CreateFeeScheduleItemInput,
    DeleteFeeScheduleItemInput,
    UpdateFeeScheduleItemInput,
)
from billing.graphql.fee_schedule_item.types import (
    FeeScheduleItemType,
)
from billing.services.fee_schedule_item_services import (
    create_fee_schedule_item as create_fee_schedule_item_service,
    delete_fee_schedule_item as delete_fee_schedule_item_service,
    update_fee_schedule_item as update_fee_schedule_item_service,
)
from billing.graphql.permissions import (
    CanCreateFeeScheduleItem,
    CanUpdateFeeScheduleItem,
    CanDeleteFeeScheduleItem,
)

@strawberry.type
class FeeScheduleItemMutation:

    @strawberry.mutation(
            permission_classes=[CanCreateFeeScheduleItem]
    )
    def create_fee_schedule_item(
        self,
        input: CreateFeeScheduleItemInput,
    ) -> FeeScheduleItemType:
        return create_fee_schedule_item_service(
            fee_schedule_id=input.fee_schedule_id,
            fee_item_id=input.fee_item_id,
            amount=input.amount,
        )

    @strawberry.mutation(
            permission_classes=[CanUpdateFeeScheduleItem]
    )
    def update_fee_schedule_item(
        self,
        input: UpdateFeeScheduleItemInput,
    ) -> FeeScheduleItemType:
        return update_fee_schedule_item_service(
            fee_schedule_item_id=input.fee_schedule_item_id,
            fee_item_id=input.fee_item_id,
            amount=input.amount,
        )

    @strawberry.mutation(
            permission_classes=[CanDeleteFeeScheduleItem]
    )
    def delete_fee_schedule_item(
        self,
        input: DeleteFeeScheduleItemInput,
    ) -> bool:
        return delete_fee_schedule_item_service(
            fee_schedule_item_id=input.fee_schedule_item_id,
        )