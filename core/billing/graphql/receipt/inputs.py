import strawberry


@strawberry.input
class CreateReceiptInput:
    payment_id: strawberry.ID
    notes: str = ""