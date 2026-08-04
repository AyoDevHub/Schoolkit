from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from accounts.models import User
from billing.models import Discount
from people.models import Student
from schools.models import (
    AcademicSession,
    AcademicTerm,
    School,
)


@transaction.atomic
def create_discount(
    *,
    school_id: str,
    student_id: str,
    academic_session_id: str,
    academic_term_id: str,
    discount_type: str,
    value_type: str,
    value: Decimal,
    reason: str = "",
    approved_by_id: str,
) -> Discount:

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

    # Validate approver exists
    try:
        approved_by = User.objects.get(
            id=approved_by_id,
        )
    except User.DoesNotExist:
        raise ValidationError({
            "approved_by":
                "Approver with the provided ID does not exist."
        })

    # Clean input
    reason = reason.strip()

    # Validate value
    if (
        value_type == Discount.ValueType.PERCENTAGE
        and (value <= 0 or value > 100)
    ):
        raise ValidationError({
            "value":
                "Percentage discount must be between 0 and 100."
        })

    if (
        value_type == Discount.ValueType.FIXED_AMOUNT
        and value <= 0
    ):
        raise ValidationError({
            "value":
                "Fixed amount discount must be greater than zero."
        })

    # Check for duplicate discount
    if Discount.objects.filter(
        school=school,
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
        discount_type=discount_type,
    ).exists():
        raise ValidationError({
            "discount":
                "A discount of this type already exists for this student in the selected academic session and term."
        })

    # Create discount
    discount = Discount(
        school=school,
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
        discount_type=discount_type,
        value_type=value_type,
        value=value,
        reason=reason,
        approved_by=approved_by,
    )

    discount.save()

    return discount


@transaction.atomic
def update_discount(
    *,
    discount_id: str,
    discount_type: str | None = None,
    value_type: str | None = None,
    value: Decimal | None = None,
    reason: str | None = None,
) -> Discount:

    # Validate discount exists
    try:
        discount = Discount.objects.get(
            id=discount_id,
        )
    except Discount.DoesNotExist:
        raise ValidationError({
            "discount_id":
                "Discount with the provided ID does not exist."
        })

    # Build new values
    new_discount_type = (
        discount_type
        if discount_type is not None
        else discount.discount_type
    )

    new_value_type = (
        value_type
        if value_type is not None
        else discount.value_type
    )

    new_value = (
        value
        if value is not None
        else discount.value
    )

    new_reason = (
        reason.strip()
        if reason is not None
        else discount.reason
    )

    # Validate value
    if (
        new_value_type == Discount.ValueType.PERCENTAGE
        and (new_value <= 0 or new_value > 100)
    ):
        raise ValidationError({
            "value":
                "Percentage discount must be between 0 and 100."
        })

    if (
        new_value_type == Discount.ValueType.FIXED_AMOUNT
        and new_value <= 0
    ):
        raise ValidationError({
            "value":
                "Fixed amount discount must be greater than zero."
        })

    # Check for duplicate
    if Discount.objects.filter(
        school=discount.school,
        student=discount.student,
        academic_session=discount.academic_session,
        academic_term=discount.academic_term,
        discount_type=new_discount_type,
    ).exclude(
        id=discount.id,
    ).exists():
        raise ValidationError({
            "discount":
                "A discount of this type already exists for this student in the selected academic session and term."
        })

    # Assign values
    discount.discount_type = new_discount_type
    discount.value_type = new_value_type
    discount.value = new_value
    discount.reason = new_reason

    discount.save()

    return discount


@transaction.atomic
def activate_discount(
    discount_id: str,
) -> Discount:

    try:
        discount = Discount.objects.get(
            id=discount_id,
        )
    except Discount.DoesNotExist:
        raise ValidationError({
            "discount_id":
                "Discount with the provided ID does not exist."
        })

    if discount.is_active:
        return discount

    discount.is_active = True
    discount.save()

    return discount


@transaction.atomic
def deactivate_discount(
    discount_id: str,
) -> Discount:

    try:
        discount = Discount.objects.get(
            id=discount_id,
        )
    except Discount.DoesNotExist:
        raise ValidationError({
            "discount_id":
                "Discount with the provided ID does not exist."
        })

    if not discount.is_active:
        return discount

    discount.is_active = False
    discount.save()

    return discount