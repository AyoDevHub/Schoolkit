from datetime import date
from django.core.exceptions import ValidationError
from django.db import transaction

from billing.models import FeeSchedule
from schools.models import School, ClassLevel, AcademicSession, AcademicTerm


@transaction.atomic
def create_fee_schedule(
    *,
    school_id: str,
    academic_session_id: str,
    academic_term_id: str,
    class_level_id: str,
    due_date: date,

) -> FeeSchedule:
    # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })

    # Validate academic session exists 
    try:
        academic_session = AcademicSession.objects.get(id=academic_session_id)
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "academic_session_id": "AcademicSession with the provided ID does not exist."
        })

    # Validate academic term exists 
    try:
        academic_term = AcademicTerm.objects.get(id=academic_term_id)
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "academic_term_id": "AcademicTerm with the provided ID does not exist."
        })

    # Validate class level exists 
    try:
        class_level = ClassLevel.objects.get(id=class_level_id)
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": "ClassLevel with the provided ID does not exist."
        })

    # Check for duplicate fee schedule
    if FeeSchedule.objects.filter(
        school=school,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
    ).exists():
        raise ValidationError(
            "A fee schedule already exists for this class level, academic session and academic term."
        )

    # Create fee schedule
    fee_schedule = FeeSchedule(
        school=school,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
        due_date=due_date,
    )

    fee_schedule.save()

    return fee_schedule


@transaction.atomic
def update_fee_schedule(
    fee_schedule_id: str,
    academic_session_id: str | None = None,
    academic_term_id: str | None = None,
    class_level_id: str | None = None,
    due_date: date | None= None,
) -> FeeSchedule:

    # Validate fee schedule exists
    try:
        fee_schedule = FeeSchedule.objects.get(
            id=fee_schedule_id,
        )
    except FeeSchedule.DoesNotExist:
        raise ValidationError({
            "fee_schedule_id":
                "FeeSchedule with the provided ID does not exist."
        })

    # Prevent modification once invoices exist
    if fee_schedule.invoices.exists():
        raise ValidationError(
            "This fee schedule has already been used to generate "
            "one or more invoices and can no longer be updated."
        )

    academic_session = fee_schedule.academic_session
    academic_term = fee_schedule.academic_term
    class_level = fee_schedule.class_level
    new_due_date = (
        due_date
        if due_date is not None
        else fee_schedule.due_date
    )

    # Validate academic session
    if academic_session_id is not None:
        try:
            academic_session = AcademicSession.objects.get(
                id=academic_session_id,
            )
        except AcademicSession.DoesNotExist:
            raise ValidationError({
                "academic_session_id":
                    "AcademicSession with the provided ID does not exist."
            })

    # Validate academic term
    if academic_term_id is not None:
        try:
            academic_term = AcademicTerm.objects.get(
                id=academic_term_id,
            )
        except AcademicTerm.DoesNotExist:
            raise ValidationError({
                "academic_term_id":
                    "AcademicTerm with the provided ID does not exist."
            })

    # Validate class level
    if class_level_id is not None:
        try:
            class_level = ClassLevel.objects.get(
                id=class_level_id,
            )
        except ClassLevel.DoesNotExist:
            raise ValidationError({
                "class_level_id":
                    "ClassLevel with the provided ID does not exist."
            })


    # Check for duplicate fee schedule
    if FeeSchedule.objects.filter(
        school=fee_schedule.school,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
    ).exclude(
        id=fee_schedule.id,
    ).exists():
        raise ValidationError(
            "A fee schedule already exists for this class level, academic session and academic term."
        )

    # Assign values
    fee_schedule.academic_session = academic_session
    fee_schedule.academic_term = academic_term
    fee_schedule.class_level = class_level
    fee_schedule.due_date = new_due_date

    fee_schedule.save()

    return fee_schedule


@transaction.atomic
def activate_fee_schedule(
    fee_schedule_id: str,
) -> FeeSchedule:
    try:
        fee_schedule = FeeSchedule.objects.get(
            id=fee_schedule_id,
        )
    except FeeSchedule.DoesNotExist:
        raise ValidationError({
            "fee_schedule_id":
                "FeeSchedule with the provided ID does not exist."
        })

    if fee_schedule.is_active:
        return fee_schedule

    fee_schedule.is_active = True
    fee_schedule.save()

    return fee_schedule


@transaction.atomic
def deactivate_fee_schedule(
    fee_schedule_id: str,
) -> FeeSchedule:
    try:
        fee_schedule = FeeSchedule.objects.get(
            id=fee_schedule_id,
        )
    except FeeSchedule.DoesNotExist:
        raise ValidationError({
            "fee_schedule_id":
                "FeeSchedule with the provided ID does not exist."
        })

    if not fee_schedule.is_active:
        return fee_schedule

    fee_schedule.is_active = False
    fee_schedule.save()

    return fee_schedule