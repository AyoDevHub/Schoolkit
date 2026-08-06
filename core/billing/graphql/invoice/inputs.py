import strawberry
from datetime import date


@strawberry.input
class CreateInvoiceInput:
    school_id: strawberry.ID
    student_id: strawberry.ID
    academic_session_id: strawberry.ID
    academic_term_id: strawberry.ID
    fee_schedule_id: strawberry.ID
    due_date: date
    notes: str = ""

@strawberry.input
class UpdateInvoiceInput:
    invoice_id: strawberry.ID
    due_date: date | None = None
    notes: str | None = None
    fee_schedule_id: strawberry.ID | None = None