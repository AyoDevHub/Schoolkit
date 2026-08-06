import strawberry

from billing.graphql.student_credit.types import (
    StudentCreditType,
)
from billing.selectors.student_credit_selectors import (
    get_student_available_credit,
    get_student_available_credit_balance,
    get_student_credit_by_id,
    list_active_student_credits,
    list_inactive_student_credits,
    list_student_credits,
    list_student_credits_by_invoice,
    list_student_credits_by_payment,
    list_student_credits_by_reason,
    list_student_credits_by_student,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class StudentCreditQuery:

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credit(
        self,
        student_credit_id: strawberry.ID,
    ) -> StudentCreditType:
        return get_student_credit_by_id(
            student_credit_id=student_credit_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credits(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_student_credits(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def active_student_credits(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_active_student_credits(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def inactive_student_credits(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_inactive_student_credits(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credits_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_student_credits_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credits_by_invoice(
        self,
        invoice_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_student_credits_by_invoice(
            invoice_id=invoice_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credits_by_payment(
        self,
        payment_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_student_credits_by_payment(
            payment_id=payment_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_credits_by_reason(
        self,
        school_id: strawberry.ID,
        reason: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentCreditType]:
        return list_student_credits_by_reason(
            school_id=school_id,
            reason=reason,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def available_student_credits(
        self,
        student_id: strawberry.ID,
    ) -> list[StudentCreditType]:
        return get_student_available_credit(
            student_id=student_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def available_student_credit_balance(
        self,
        student_id: strawberry.ID,
    ) -> float:
        return float(
            get_student_available_credit_balance(
                student_id=student_id,
            )
        )