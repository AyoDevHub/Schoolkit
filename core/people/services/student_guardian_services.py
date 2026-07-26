from django.core.exceptions import ValidationError
from django.db import transaction

from people.models import (
    Guardian,
    Student,
    StudentGuardian,
)


@transaction.atomic
def create_student_guardian(
    *,
    student_id: str,
    guardian_id: str,
    relationship: str,
    is_primary: bool = False,
) -> StudentGuardian:

    # Validate student exists
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id": "Student with the provided ID does not exist."
        })

    # Validate guardian exists
    try:
        guardian = Guardian.objects.get(id=guardian_id)
    except Guardian.DoesNotExist:
        raise ValidationError({
            "guardian_id": "Guardian with the provided ID does not exist."
        })

    # Validate guardian is active
    if not guardian.is_active:
        raise ValidationError({
            "guardian_id": (
                "Cannot link an inactive guardian."
            )
        })

    # Validate student and guardian belong to the same school
    if student.school != guardian.school:
        raise ValidationError({
            "guardian_id": (
                "Student and guardian must belong to the same school."
            )
        })

    # Validate duplicate relationship
    if StudentGuardian.objects.filter(
        student=student,
        guardian=guardian,
    ).exists():
        raise ValidationError({
            "guardian_id": (
                "This guardian is already linked to the student."
            )
        })

    # Validate only one primary guardian
    if (
        is_primary
        and StudentGuardian.objects.filter(
            student=student,
            is_primary=True,
            is_active=True,
        ).exists()
    ):
        raise ValidationError({
            "is_primary": (
                "This student already has a primary guardian."
            )
        })

    # Create relationship
    student_guardian = StudentGuardian(
        student=student,
        guardian=guardian,
        relationship=relationship,
        is_primary=is_primary,
    )

    student_guardian.save()

    return student_guardian


@transaction.atomic
def update_student_guardian(
    *,
    student_guardian_id: str,
    relationship: str | None = None,
    is_primary: bool | None = None,
) -> StudentGuardian:

    # Validate relationship exists
    try:
        student_guardian = StudentGuardian.objects.get(
            id=student_guardian_id,
        )
    except StudentGuardian.DoesNotExist:
        raise ValidationError({
            "student_guardian_id": (
                "Student guardian relationship with the provided ID does not exist."
            )
        })

    # Build new values
    new_relationship = (
        relationship
        if relationship is not None
        else student_guardian.relationship
    )

    new_is_primary = (
        is_primary
        if is_primary is not None
        else student_guardian.is_primary
    )

    # Validate only one primary guardian
    if (
        new_is_primary
        and StudentGuardian.objects.filter(
            student=student_guardian.student,
            is_primary=True,
            is_active=True,
        ).exclude(
            id=student_guardian.id,
        ).exists()
    ):
        raise ValidationError({
            "is_primary": (
                "This student already has a primary guardian."
            )
        })

    # Assign values
    student_guardian.relationship = new_relationship
    student_guardian.is_primary = new_is_primary

    student_guardian.save()

    return student_guardian


@transaction.atomic
def activate_student_guardian(
    *,
    student_guardian_id: str,
) -> StudentGuardian:

    # Validate relationship exists
    try:
        student_guardian = StudentGuardian.objects.get(
            id=student_guardian_id,
        )
    except StudentGuardian.DoesNotExist:
        raise ValidationError({
            "student_guardian_id": (
                "Student guardian relationship with the provided ID does not exist."
            )
        })

    # Already active
    if student_guardian.is_active:
        return student_guardian

    # Validate only one active primary guardian
    if (
        student_guardian.is_primary
        and StudentGuardian.objects.filter(
            student=student_guardian.student,
            is_primary=True,
            is_active=True,
        ).exclude(
            id=student_guardian.id,
        ).exists()
    ):
        raise ValidationError({
            "is_primary": (
                "This student already has an active primary guardian."
            )
        })

    student_guardian.is_active = True
    student_guardian.save()

    return student_guardian


@transaction.atomic
def deactivate_student_guardian(
    *,
    student_guardian_id: str,
) -> StudentGuardian:

    # Validate relationship exists
    try:
        student_guardian = StudentGuardian.objects.get(
            id=student_guardian_id,
        )
    except StudentGuardian.DoesNotExist:
        raise ValidationError({
            "student_guardian_id": (
                "Student guardian relationship with the provided ID does not exist."
            )
        })

    # Already inactive
    if not student_guardian.is_active:
        return student_guardian

    student_guardian.is_active = False
    student_guardian.save()

    return student_guardian