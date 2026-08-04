import strawberry

from billing.graphql.fee_schedule.inputs import (
    ActivateFeeScheduleInput,
    CreateFeeScheduleInput,
    DeactivateFeeScheduleInput,
    UpdateFeeScheduleInput,
)
from billing.graphql.fee_schedule.types import FeeScheduleType
from billing.services.fee_schedule_services import (
    activate_fee_schedule as activate_fee_schedule_service,
    create_fee_schedule as create_fee_schedule_service,
    deactivate_fee_schedule as deactivate_fee_schedule_service,
    update_fee_schedule as update_fee_schedule_service,
)
from billing.graphql.permissions import (
    CanCreateFeeSchedule,
    CanUpdateFeeSchedule,
    CanDeactivateFeeSchedule,
    CanActivateFeeSchedule,
)

@strawberry.type
class FeeScheduleMutation:

    @strawberry.mutation(
            permission_classes=[CanCreateFeeSchedule]
    )
    def create_fee_schedule(
        self,
        input: CreateFeeScheduleInput,
    ) -> FeeScheduleType:
        return create_fee_schedule_service(
            school_id=input.school_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            class_level_id=input.class_level_id,
            due_date=input.due_date,
        )

    @strawberry.mutation(
            permission_classes=[CanUpdateFeeSchedule]
    )
    def update_fee_schedule(
        self,
        input: UpdateFeeScheduleInput,
    ) -> FeeScheduleType:
        return update_fee_schedule_service(
            fee_schedule_id=input.fee_schedule_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            class_level_id=input.class_level_id,
            due_date=input.due_date,
        )

    @strawberry.mutation(
            permission_classes=[CanActivateFeeSchedule]
    )
    def activate_fee_schedule(
        self,
        input: ActivateFeeScheduleInput,
    ) -> FeeScheduleType:
        return activate_fee_schedule_service(
            fee_schedule_id=input.fee_schedule_id,
        )

    @strawberry.mutation(
            permission_classes=[CanDeactivateFeeSchedule]
    )
    def deactivate_fee_schedule(
        self,
        input: DeactivateFeeScheduleInput,
    ) -> FeeScheduleType:
        return deactivate_fee_schedule_service(
            fee_schedule_id=input.fee_schedule_id,
        )