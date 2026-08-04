import strawberry
from strawberry.types import Info

from billing.graphql.discount.inputs import (
    CreateDiscountInput,
    UpdateDiscountInput,
    ActivateDiscountInput,
    DeactivateDiscountInput,
)

from billing.graphql.discount.types import DiscountType

from billing.services.discount_services import (
    create_discount as create_discount_service,
    update_discount as update_discount_service,
    activate_discount as activate_discount_service,
    deactivate_discount as deactivate_discount_service,
)
from billing.graphql.permissions import (
    CanActivateDiscount,
    CanUpdateDiscount,
    CanDeactivateDiscount,
    CanCreateDiscount,
)

@strawberry.type
class DiscountMutation:

    @strawberry.mutation(
            permission_classes=[CanCreateDiscount]
    )
    def create_discount(
        self,
        info: Info,
        input: CreateDiscountInput,
    ) -> DiscountType:

        return create_discount_service(
            school_id=input.school_id,
            student_id=input.student_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            discount_type=input.discount_type,
            value_type=input.value_type,
            value=input.value,
            reason=input.reason,
            approved_by_id=info.context.user.id,
        )

    @strawberry.mutation(
            permission_classes=[CanUpdateDiscount]
    )
    def update_discount(
        self,
        input: UpdateDiscountInput,
    ) -> DiscountType:

        return update_discount_service(
            discount_id=input.discount_id,
            discount_type=input.discount_type,
            value_type=input.value_type,
            value=input.value,
            reason=input.reason,
        )

    @strawberry.mutation(
            permission_classes=[CanActivateDiscount]
    )
    def activate_discount(
        self,
        input: ActivateDiscountInput,
    ) -> DiscountType:

        return activate_discount_service(
            discount_id=input.discount_id,
        )

    @strawberry.mutation(
            permission_classes=[CanDeactivateDiscount]
    )
    def deactivate_discount(
        self,
        input: DeactivateDiscountInput,
    ) -> DiscountType:

        return deactivate_discount_service(
            discount_id=input.discount_id,
        )