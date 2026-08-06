import strawberry

from billing.graphql.receipt.inputs import (
    CreateReceiptInput,
)
from billing.graphql.receipt.types import (
    ReceiptType,
)
from billing.selectors.payment_selectors import (
    get_payment_by_id,
)
from billing.services.receipt_service import (
    create_receipt,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class ReceiptMutation:

    @strawberry.mutation(
            permission_classes=[IsFinanceOfficer],
    )
    def create_receipt(
        self,
        input: CreateReceiptInput,
    ) -> ReceiptType:

        payment = get_payment_by_id(
            payment_id=input.payment_id,
        )

        return create_receipt(
            payment=payment,
            notes=input.notes,
        )