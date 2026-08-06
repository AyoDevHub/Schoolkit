import strawberry

from billing.graphql.payment.types import PaymentType
from billing.selectors.payment_selectors import (
    get_payment_by_id,
    list_payments,
    list_payments_by_invoice,
    list_payments_by_student,
    get_payment_by_reference,
    list_payments_by_status,
    list_payments_by_method,
)


@strawberry.type
class PaymentQuery:

    @strawberry.field
    def payment(
        self,
        id: strawberry.ID,
    ) -> PaymentType | None:
        return get_payment_by_id(
            id=id,
        )

    @strawberry.field
    def payments(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PaymentType]:
        return list_payments(
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def payments_by_invoice(
        self,
        invoice_id: strawberry.ID,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PaymentType]:
        return list_payments_by_invoice(
            invoice_id=invoice_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def payments_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PaymentType]:
        return list_payments_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def payment_by_reference(
        self,
        reference: str,
    ) -> PaymentType:
        return get_payment_by_reference(
            reference=reference,
        )


    @strawberry.field
    def payments_by_status(
        self,
        school_id: strawberry.ID,
        status: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PaymentType]:
        return list_payments_by_status(
            school_id=school_id,
            status=status,
            offset=offset,
            limit=limit,
        )


    @strawberry.field
    def payments_by_method(
        self,
        school_id: strawberry.ID,
        payment_method: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[PaymentType]:
        return list_payments_by_method(
            school_id=school_id,
            payment_method=payment_method,
            offset=offset,
            limit=limit,
        )