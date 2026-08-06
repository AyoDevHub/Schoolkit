import strawberry
from decimal import Decimal

from billing.graphql.student_credit.enums import StudentCreditReasonEnum


@strawberry.input
class CreateStudentCreditInput:
    amount: Decimal
    reason: StudentCreditReasonEnum 
    payment_id: strawberry.ID | None = None
    invoice_id: strawberry.ID | None = None
    notes: str = ""