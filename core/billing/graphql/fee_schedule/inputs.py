import strawberry

from datetime import date

@strawberry.input
class CreateFeeScheduleInput:
    school_id: strawberry.ID
    academic_session_id: strawberry.ID
    academic_term_id: strawberry.ID
    class_level_id: strawberry.ID
    due_date: date


@strawberry.input
class UpdateFeeScheduleInput:
    fee_schedule_id: strawberry.ID
    academic_session_id: strawberry.ID | None = None
    academic_term_id: strawberry.ID | None = None
    class_level_id: strawberry.ID | None = None
    due_date: date | None = None 


@strawberry.input
class ActivateFeeScheduleInput:
    fee_schedule_id: strawberry.ID


@strawberry.input
class DeactivateFeeScheduleInput:
    fee_schedule_id: strawberry.ID