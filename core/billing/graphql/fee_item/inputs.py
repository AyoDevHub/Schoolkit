import strawberry


@strawberry.input
class CreateFeeItemInput:
    school_id: strawberry.ID
    name: str
    description: str = ""
    is_recurring: bool

@strawberry.input
class UpdateFeeItemInput:
    fee_item_id: strawberry.ID
    name: str | None = None
    description: str | None = None
    is_recurring: bool | None = None


@strawberry.input
class ActivateFeeItemInput:
    fee_item_id: strawberry.ID


@strawberry.input
class DeactivateFeeItemInput:
    fee_item_id: strawberry.ID