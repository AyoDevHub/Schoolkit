import strawberry

from billing.graphql.invoice.inputs import (
    CreateInvoiceInput,
    UpdateInvoiceInput,
)
from billing.graphql.invoice.types import InvoiceType
from billing.services.invoice_services import (
    create_invoice,
    update_invoice,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class InvoiceMutation:

    @strawberry.mutation(
            permission_classes=[IsFinanceOfficer]
    )
    def create_invoice(
        self,
        input: CreateInvoiceInput,
    ) -> InvoiceType:

        return create_invoice(
            school_id=input.school_id,
            student_id=input.student_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            fee_schedule_id=input.fee_schedule_id,
            due_date=input.due_date,
            notes=input.notes,
        )

    @strawberry.mutation(
            permission_classes=[IsFinanceOfficer]
    )
    def update_invoice(
        self,
        input: UpdateInvoiceInput,
    ) -> InvoiceType:

        return update_invoice(
            invoice_id=input.invoice_id,
            due_date=input.due_date,
            notes=input.notes,
            fee_schedule_id=input.fee_schedule_id,
        )