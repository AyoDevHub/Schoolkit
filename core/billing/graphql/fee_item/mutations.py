import strawberry

from billing.graphql.fee_item.inputs import (
    CreateFeeItemInput,
    UpdateFeeItemInput,
    ActivateFeeItemInput,
    DeactivateFeeItemInput,
)
from billing.graphql.fee_item.types import FeeItemType
from billing.services.fee_item_services import (
    create_fee_item as create_fee_item_service,
    update_fee_item as update_fee_item_service,
    deactivate_fee_item as deactivate_fee_item_service,
    activate_fee_item as activate_fee_item_service,
)
from billing.graphql.permissions import (
    CanCreateFeeItem,
    CanUpdateFeeItem,
    CanActivateFeeItem,
    CanDeactivateFeeItem,
)


@strawberry.type
class FeeItemMutation:

    @strawberry.mutation(
        permission_classes=[CanCreateFeeItem]
    )
    def create_fee_item(
        self,
        input: CreateFeeItemInput,
    ) -> FeeItemType:
        return create_fee_item_service(
            school_id=input.school_id,
            name=input.name,
            description=input.description,
            is_recurring=input.is_recurring,
        )

    @strawberry.mutation(
        permission_classes=[CanUpdateFeeItem]
    )
    def update_fee_item(
        self,
        input: UpdateFeeItemInput,
    ) -> FeeItemType:
        return update_fee_item_service(
            fee_item_id=input.fee_item_id,
            name=input.name,
            description=input.description,
            is_recurring=input.is_recurring,
        )

    @strawberry.mutation(
        permission_classes=[CanActivateFeeItem]
    )
    def activate_fee_item(
        self,
        input: ActivateFeeItemInput,
    ) -> FeeItemType:
        return activate_fee_item_service(
            fee_item_id=input.fee_item_id,
        )

    @strawberry.mutation(
        permission_classes=[CanDeactivateFeeItem]
    )
    def deactivate_fee_item(
        self,
        input: DeactivateFeeItemInput,
    ) -> FeeItemType:
        return deactivate_fee_item_service(
            fee_item_id=input.fee_item_id,
        )