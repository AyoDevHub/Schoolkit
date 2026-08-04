from decimal import Decimal
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from schools.models import (
    AcademicSession,
    AcademicTerm,
    School,
)

from people.models import Student

from billing.models import (
    FeeSchedule,
    Discount,
    FeeScheduleItem,
    Invoice,
    InvoiceLine,
    LedgerEntry,
    LedgerEntryType,
    LedgerTransactionType,
    ValueType,
    InvoiceStatus,
)


@transaction.atomic
def create_invoice(
    *,
    school_id: str,
    student_id: str,
    academic_session_id: str,
    academic_term_id: str,
    fee_schedule_id: str,
    due_date: date,
    notes: str = "",
):


    # Validate school exists
    try:
        school = School.objects.get(
            id=school_id,
        )
    except School.DoesNotExist:
        raise ValidationError({
            "school_id":
                "School with the provided ID does not exist."
        })


    # Validate student exists
    try:
        student = Student.objects.get(
            id=student_id,
        )
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id":
                "Student with the provided ID does not exist."
        })
    
    # Validate academic session exists
    try:
        academic_session = AcademicSession.objects.get(
            id=academic_session_id,
        )
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "academic_session_id":
                "AcademicSession with the provided ID does not exist."
        })
    
    # Validate academic term exists
    try:
        academic_term = AcademicTerm.objects.get(
            id=academic_term_id,
        )
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "academic_term_id":
                "AcademicTerm with the provided ID does not exist."
        })
    
    # Validate fee schedule exists 
    try:
        fee_schedule = FeeSchedule.objects.get(
            id=fee_schedule_id,
        )
    except FeeSchedule.DoesNotExist:
        raise ValidationError({
            "fee_schedule_id":
                "Fee Schedule with the provided ID does not exist."
        })

    # Validate relationships
    if student.school_id != school.id:
        raise ValidationError({
            "student_id": (
                "The student does not belong to the selected school."
            )
        })

    if fee_schedule.school_id != school.id:
        raise ValidationError({
            "fee_schedule_id": (
                "The fee schedule does not belong to the selected school."
            )
        })
    
    if fee_schedule.academic_session_id != academic_session.id:
        raise ValidationError({
            "fee_schedule_id": (
                "The fee schedule does not belong "
                "to the selected academic session."
            )
        })

    if fee_schedule.academic_term_id != academic_term.id:
        raise ValidationError({
            "fee_schedule_id": (
                "The fee schedule does not belong "
                "to the selected academic term."
            )
        })

    if academic_session.school_id != school.id:
        raise ValidationError({
            "academic_session_id": (
                "The academic session does not belong to the selected school."
            )
        })

    if academic_term.school_id != school.id:
        raise ValidationError({
            "academic_term_id": (
                "The academic term does not belong to the selected school."
            )
        })

    if academic_term.academic_session_id != academic_session.id:
        raise ValidationError({
            "academic_term_id": (
                "The selected term does not belong "
                "to the selected academic session."
            )
        })

     #Check student status 
    if not student.is_active:
        raise ValidationError({
            "student_id": (
                "Invoices cannot be generated for inactive students."
            )
        })
    
    if due_date < academic_term.start_date:
        raise ValidationError({
            "due_date": (
                "The due date cannot be earlier than "
                "the academic term start date."
            )
        })

        
    # Check for duplicates
    if Invoice.objects.filter(
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
    ).exists():
        raise ValidationError(
            "An invoice already exists for this student "
            "in the selected session and term."
        )

    # Generate an invoice number 
    invoice_count = Invoice.objects.count() + 1

    invoice_number = (
        f"INV-{academic_session.start_date.year}-{invoice_count:06d}"
    )

    subtotal = Decimal("0.00")
        
    fee_schedule_items = FeeScheduleItem.objects.filter(
        fee_schedule=fee_schedule,
    ).order_by("fee_item__name")
         
    if not fee_schedule_items.exists():
        raise ValidationError(
            "The selected fee schedule has no fee items."
        )

    #Validate fee schedule is active
    if not fee_schedule.is_active:
        raise ValidationError({
            "fee_schedule_id": (
                "Invoices can only be generated from an active fee schedule."
            )
        })
    
    # Create Invoice
    invoice = Invoice.objects.create(
        school=school,
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
        fee_schedule=fee_schedule,
        invoice_number=invoice_number,
        due_date=due_date,
        notes=notes,
    )

    # Create invoice line 
    for schedule_item in fee_schedule_items:
    
        InvoiceLine.objects.create(
            invoice=invoice,
            fee_item=schedule_item.fee_item,
            amount=schedule_item.amount,
        )
    
        subtotal += schedule_item.amount

    # Apply Discount
    discount_total = Decimal("0.00")

    discounts = Discount.objects.filter(
        school=school,
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
        is_active=True,
    )

    for discount in discounts:

        if discount.value_type == ValueType.PERCENTAGE:
          # Quantize result to avoid decimal precision
          discount_amount = (
              subtotal * discount.value
          ) / Decimal("100")

          discount_total += discount_amount.quantize(
              Decimal("0.01")
          )

        else:
            discount_total += discount.value

    if discount_total > subtotal:
        discount_total = subtotal

    total_amount = subtotal - discount_total

    # Update invoice totals
    invoice.subtotal = subtotal
    invoice.discount_total = discount_total
    invoice.total_amount = total_amount

    invoice.save(
        update_fields=[
            "subtotal",
            "discount_total",
            "total_amount",
            "updated_at",
        ],
    )

    # Create ledger entry
    LedgerEntry.objects.create(
        student=student,
        invoice=invoice,
        entry_type=LedgerEntryType.DEBIT,
        transaction_type=LedgerTransactionType.INVOICE,
        amount=total_amount,
    )

    return invoice




@transaction.atomic
def update_invoice(
    *,
    invoice_id: str,
    due_date: date | None = None,
    notes: str | None = None,
    fee_schedule_id: str | None = None,
):
    # Validate invoice exists
    try:
        invoice = Invoice.objects.get(
            id=invoice_id,
        )
    except Invoice.DoesNotExist:
        raise ValidationError({
            "invoice_id": (
                "Invoice with the provided ID does not exist."
            )
        })

    # Only unpaid invoices can be updated
    if invoice.status != InvoiceStatus.UNPAID:
        raise ValidationError(
            "Only unpaid invoices can be updated."
        )

    update_fields = [
        "updated_at",
    ]

    # Update due date
    if due_date is not None:

        if due_date < invoice.academic_term.start_date:
            raise ValidationError({
                "due_date": (
                    "The due date cannot be earlier than "
                    "the academic term start date."
                )
            })

        invoice.due_date = due_date
        update_fields.append("due_date")

    # Update notes
    if notes is not None:
        invoice.notes = notes
        update_fields.append("notes")

    # Update fee schedule if supplied
    if (
        fee_schedule_id is not None
        and fee_schedule_id != str(invoice.fee_schedule_id)
    ):

        # Validate fee schedule exists
        try:
            fee_schedule = FeeSchedule.objects.get(
                id=fee_schedule_id,
            )
        except FeeSchedule.DoesNotExist:
            raise ValidationError({
                "fee_schedule_id": (
                    "Fee Schedule with the provided ID "
                    "does not exist."
                )
            })

        # Validate relationships
        if fee_schedule.school_id != invoice.school_id:
            raise ValidationError({
                "fee_schedule_id": (
                    "The fee schedule does not belong "
                    "to the invoice school."
                )
            })

        if (
            fee_schedule.academic_session_id
            != invoice.academic_session_id
        ):
            raise ValidationError({
                "fee_schedule_id": (
                    "The fee schedule does not belong "
                    "to the invoice academic session."
                )
            })

        if (
            fee_schedule.academic_term_id
            != invoice.academic_term_id
        ):
            raise ValidationError({
                "fee_schedule_id": (
                    "The fee schedule does not belong "
                    "to the invoice academic term."
                )
            })

        # Get fee schedule items
        fee_schedule_items = FeeScheduleItem.objects.filter(
            fee_schedule=fee_schedule,
        )

        if not fee_schedule_items.exists():
            raise ValidationError({
                "fee_schedule_id": (
                    "The selected fee schedule "
                    "has no fee items."
                )
            })

        # Delete existing invoice lines
        invoice.invoice_lines.all().delete()

        # Recreate invoice lines
        subtotal = Decimal("0.00")

        for schedule_item in fee_schedule_items:

            InvoiceLine.objects.create(
                invoice=invoice,
                fee_item=schedule_item.fee_item,
                amount=schedule_item.amount,
            )

            subtotal += schedule_item.amount

        # Apply discounts
        discount_total = Decimal("0.00")

        discounts = Discount.objects.filter(
            school=invoice.school,
            student=invoice.student,
            academic_session=invoice.academic_session,
            academic_term=invoice.academic_term,
            is_active=True,
        )

        for discount in discounts:

            if discount.value_type == ValueType.PERCENTAGE:

                discount_amount = (
                    subtotal * discount.value
                ) / Decimal("100")

                discount_total += discount_amount.quantize(
                    Decimal("0.01")
                )

            else:
                discount_total += discount.value

        if discount_total > subtotal:
            discount_total = subtotal

        total_amount = subtotal - discount_total

        # Update invoice totals
        invoice.fee_schedule = fee_schedule
        invoice.subtotal = subtotal
        invoice.discount_total = discount_total
        invoice.total_amount = total_amount

        update_fields.extend([
            "fee_schedule",
            "subtotal",
            "discount_total",
            "total_amount",
        ])

        # Update corresponding ledger entry
        try:
            ledger_entry = LedgerEntry.objects.get(
                invoice=invoice,
                transaction_type=LedgerTransactionType.INVOICE,
            )
        except LedgerEntry.DoesNotExist:
            raise ValidationError({
                "invoice_id": (
                    "The invoice has no corresponding ledger entry."
                )
            })

        ledger_entry.amount = total_amount

        ledger_entry.save(
            update_fields=[
                "amount",
                "updated_at",
            ],
        )

    # Save invoice
    invoice.save(
        update_fields=update_fields,
    )

    return invoice
    