import strawberry

from billing.graphql.receipt.types import (
    ReceiptType,
)
from billing.selectors.receipt_selectors import (
    get_receipt_by_id,
    get_receipt_by_number,
    get_receipt_by_payment,
    list_receipts,
    list_receipts_by_student,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class ReceiptQuery:

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def receipt(
        self,
        receipt_id: strawberry.ID,
    ) -> ReceiptType:
        return get_receipt_by_id(
            receipt_id=receipt_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def receipt_by_number(
        self,
        receipt_number: str,
    ) -> ReceiptType:
        return get_receipt_by_number(
            receipt_number=receipt_number,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def receipt_by_payment(
        self,
        payment_id: strawberry.ID,
    ) -> ReceiptType:
        return get_receipt_by_payment(
            payment_id=payment_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def receipts(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[ReceiptType]:
        return list_receipts(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def receipts_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[ReceiptType]:
        return list_receipts_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )