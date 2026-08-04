import strawberry

from billing.graphql.fee_schedule.types import FeeScheduleType
from billing.selectors.fee_schedule_selectors import (
    get_fee_schedule_by_id,
    list_fee_schedules,
)
from billing.graphql.permissions import CanViewFeeSchedule

@strawberry.type
class FeeScheduleQuery:

    @strawberry.field(
            permission_classes=[CanViewFeeSchedule]
    )
    def fee_schedule(
        self,
        id: strawberry.ID,
    ) -> FeeScheduleType | None:
        return get_fee_schedule_by_id(id)

    @strawberry.field(
            permission_classes=[CanViewFeeSchedule]
    )
    def fee_schedules(
        self,
        school_id: strawberry.ID,
        academic_session_id: strawberry.ID | None = None,
        academic_term_id: strawberry.ID | None = None,
        class_level_id: strawberry.ID | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> list[FeeScheduleType]:
        return list_fee_schedules(
            school_id=school_id,
            academic_session_id=academic_session_id,
            academic_term_id=academic_term_id,
            class_level_id=class_level_id,
            is_active=is_active,
            offset=offset,
            limit=limit,
        )