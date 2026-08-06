import strawberry

from billing.graphql.invoice.types import InvoiceType
from billing.selectors.invoice_selectors import (
    get_invoice_by_id,
    get_invoice_by_number,
    list_invoices,
    list_invoices_by_session,
    list_invoices_by_status,
    list_invoices_by_student,
    list_invoices_by_term,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class InvoiceQuery:

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoice(
        self,
        invoice_id: strawberry.ID,
    ) -> InvoiceType:
        return get_invoice_by_id(
            invoice_id=invoice_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoice_by_number(
        self,
        invoice_number: str,
    ) -> InvoiceType:
        return get_invoice_by_number(
            invoice_number=invoice_number,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoices(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InvoiceType]:
        return list_invoices(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoices_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InvoiceType]:
        return list_invoices_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoices_by_session(
        self,
        academic_session_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InvoiceType]:
        return list_invoices_by_session(
            academic_session_id=academic_session_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoices_by_term(
        self,
        academic_term_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InvoiceType]:
        return list_invoices_by_term(
            academic_term_id=academic_term_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer]
    )
    def invoices_by_status(
        self,
        school_id: strawberry.ID,
        status: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[InvoiceType]:
        return list_invoices_by_status(
            school_id=school_id,
            status=status,
            offset=offset,
            limit=limit,
        )