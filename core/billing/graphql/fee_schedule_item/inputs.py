import decimal

import strawberry


@strawberry.input
class CreateFeeScheduleItemInput:
    fee_schedule_id: strawberry.ID
    fee_item_id: strawberry.ID
    amount: decimal.Decimal


@strawberry.input
class UpdateFeeScheduleItemInput:
    fee_schedule_item_id: strawberry.ID
    fee_item_id: strawberry.ID | None = None
    amount: decimal.Decimal | None = None


@strawberry.input
class DeleteFeeScheduleItemInput:
    fee_schedule_item_id: strawberry.ID