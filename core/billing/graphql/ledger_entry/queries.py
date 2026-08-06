import strawberry

from billing.graphql.ledger_entry.types import (
    LedgerEntryType,
)
from billing.selectors.ledger_entry_selectors import (
    get_ledger_entry_by_id,
    get_student_balance,
    list_ledger_entries,
    list_ledger_entries_by_discount,
    list_ledger_entries_by_entry_type,
    list_ledger_entries_by_invoice,
    list_ledger_entries_by_payment,
    list_ledger_entries_by_student,
    list_ledger_entries_by_student_credit,
    list_ledger_entries_by_transaction_type,
)
from billing.graphql.permissions import IsFinanceOfficer

@strawberry.type
class LedgerEntryQuery:

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
        )
    def ledger_entry(
        self,
        ledger_entry_id: strawberry.ID,
    ) -> LedgerEntryType:
        return get_ledger_entry_by_id(
            ledger_entry_id=ledger_entry_id,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_invoice(
        self,
        invoice_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_invoice(
            invoice_id=invoice_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_payment(
        self,
        payment_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_payment(
            payment_id=payment_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_discount(
        self,
        discount_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_discount(
            discount_id=discount_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_student_credit(
        self,
        student_credit_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_student_credit(
            student_credit_id=student_credit_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_transaction_type(
        self,
        school_id: strawberry.ID,
        transaction_type: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_transaction_type(
            school_id=school_id,
            transaction_type=transaction_type,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def ledger_entries_by_entry_type(
        self,
        school_id: strawberry.ID,
        entry_type: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[LedgerEntryType]:
        return list_ledger_entries_by_entry_type(
            school_id=school_id,
            entry_type=entry_type,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
            permission_classes=[IsFinanceOfficer],
    )
    def student_balance(
        self,
        student_id: strawberry.ID,
    ) -> float:
        return float(
            get_student_balance(
                student_id=student_id,
            )
        )