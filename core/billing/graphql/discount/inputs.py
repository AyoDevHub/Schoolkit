import strawberry

from billing.models import Discount
from billing.graphql.discount.enums import ValueTypeEnum, DiscountCategoryEnum

@strawberry.input
class CreateDiscountInput:
    school_id: strawberry.ID
    student_id: strawberry.ID
    academic_session_id: strawberry.ID
    academic_term_id: strawberry.ID
    discount_type: DiscountCategoryEnum
    value_type: ValueTypeEnum
    value: float
    reason: str = ""


@strawberry.input
class UpdateDiscountInput:
    discount_id: strawberry.ID
    discount_type: DiscountCategoryEnum | None = None
    value_type: ValueTypeEnum | None = None
    value: float | None = None
    reason: str | None = None


@strawberry.input
class ActivateDiscountInput:
    discount_id: strawberry.ID


@strawberry.input
class DeactivateDiscountInput:
    discount_id: strawberry.ID