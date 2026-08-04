import strawberry

from billing.graphql.discount.types import DiscountType
from billing.selectors.discount_selectors import (
    get_discount_by_id,
    list_discounts,
    list_active_discounts,
    list_inactive_discounts,
    list_discounts_by_student,
)
from billing.graphql.permissions import CanViewDiscount

@strawberry.type
class DiscountQuery:

    @strawberry.field(
            permission_classes=[CanViewDiscount]
    )
    def discount(
        self,
        id: strawberry.ID,
    ) -> DiscountType | None:
        return get_discount_by_id(id)

    @strawberry.field(
            permission_classes=[CanViewDiscount]
    )
    def discounts(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DiscountType]:
        return list_discounts(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[CanViewDiscount]
    )
    def active_discounts(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DiscountType]:
        return list_active_discounts(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[CanViewDiscount]
    )
    def inactive_discounts(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DiscountType]:
        return list_inactive_discounts(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[CanViewDiscount]
    )
    def discounts_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DiscountType]:
        return list_discounts_by_student(
            student_id,
            offset=offset,
            limit=limit,
        )