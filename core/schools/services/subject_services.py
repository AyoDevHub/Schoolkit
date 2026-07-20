from django.db import transaction
from django.core.exceptions import ValidationError

from schools.models import (
    School,
    Subject,
    ClassLevel,
)


@transaction.atomic
def create_subject(
    *,
    school_id: str,
    name: str,
    level_ids: list[str],
) -> Subject:
    # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })

    # Clean name
    name = name.strip()

    # Validate empty name
    if not name:
        raise ValidationError({
            "name": "Subject name cannot be empty."
        })

    # Validate duplicate subject
    if Subject.objects.filter(
        school=school,
        name__iexact=name,
    ).exists():
        raise ValidationError({
            "name": "A subject with this name already exists for this school."
        })

    # Validate at least one level
    if not level_ids:
        raise ValidationError({
            "levels": "At least one class level must be assigned to the subject."
        })

    # Fetch levels
    levels = ClassLevel.objects.filter(
        id__in=level_ids,
    )

    # Validate all levels exist
    if len(levels) != len(level_ids):
        raise ValidationError({
            "levels": "One or more class levels do not exist."
        })

    # Validate all levels belong to the school
    for level in levels:
        if level.school_id != school.id:
            raise ValidationError({
                "levels": (
                    "All selected class levels must belong to the specified school."
                )
            })

    # Create subject
    subject = Subject(
        school=school,
        name=name,
    )

    subject.save()

    # Assign levels
    subject.levels.set(levels)

    return subject




@transaction.atomic
def update_subject(
    *,
    subject_id: str,
    name: str | None = None,
    level_ids: list[str] | None = None,
) -> Subject:

    # Validate subject exists
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        raise ValidationError({
            "subject_id": "Subject with the provided ID does not exist."
        })

    # Build new name
    new_name = (
        name.strip()
        if name is not None
        else subject.name
    )

    # Validate empty name
    if not new_name:
        raise ValidationError({
            "name": "Subject name cannot be empty."
        })

    # Validate duplicate
    if Subject.objects.filter(
        school=subject.school,
        name__iexact=new_name,
    ).exclude(
        id=subject.id,
    ).exists():
        raise ValidationError({
            "name": "A subject with this name already exists for this school."
        })

    # Validate levels (only if supplied)
    if level_ids is not None:

        # At least one level
        if not level_ids:
            raise ValidationError({
                "levels": "At least one class level must be assigned to the subject."
            })

        # Fetch levels
        levels = ClassLevel.objects.filter(
            id__in=level_ids,
        )

        # Validate all levels exist
        if len(levels) != len(level_ids):
            raise ValidationError({
                "levels": "One or more class levels do not exist."
            })

        # Validate all belong to the same school
        for level in levels:
            if level.school_id != subject.school_id:
                raise ValidationError({
                    "levels": (
                        "All selected class levels must belong to the subject's school."
                    )
                })

    # Assign values
    subject.name = new_name

    subject.save()

    # Update level mappings
    if level_ids is not None:
        subject.levels.set(levels)

    return subject