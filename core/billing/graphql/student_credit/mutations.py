import strawberry

from billing.graphql.student_credit.inputs import (
    CreateStudentCreditInput,
)
from billing.graphql.student_credit.types import (
    StudentCreditType,
)
from billing.selectors.invoice_selectors import (
    get_invoice_by_id,
)
from billing.selectors.payment_selectors import (
    get_payment_by_id,
)
from billing.services.student_credit_service import (
    create_student_credit,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class StudentCreditMutation:

    @strawberry.mutation(
            permission_classes=[IsFinanceOfficer],
    )
    def create_student_credit(
        self,
        input: CreateStudentCreditInput,
    ) -> StudentCreditType:

        payment = (
            get_payment_by_id(
                payment_id=input.payment_id,
            )
            if input.payment_id
            else None
        )

        invoice = (
            get_invoice_by_id(
                invoice_id=input.invoice_id,
            )
            if input.invoice_id
            else None
        )

        return create_student_credit(
            amount=input.amount,
            reason=input.reason,
            payment=payment,
            invoice=invoice,
            notes=input.notes,
        )