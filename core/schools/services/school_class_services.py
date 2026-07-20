from django.db import transaction
from django.core.exceptions import ValidationError

from schools.models import School, ClassLevel, ClassArm


# -------- Class Level --------

@transaction.atomic
def create_class_level(
    *,
    school_id: str,
    name: str,
) -> ClassLevel:

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
            "name": "Class level name cannot be empty."
        })

    # Validate duplicate
    if ClassLevel.objects.filter(
        school=school,
        name__iexact=name,
    ).exists():
        raise ValidationError({
            "name": "A class level with this name already exists for this school."
        })

    level = ClassLevel(
        school=school,
        name=name,
    )

    level.save()

    return level




@transaction.atomic
def update_class_level(
    *,
    class_level_id: str,
    name: str | None = None,
) -> ClassLevel:
    # Validate class level exists
    try:
        level = ClassLevel.objects.get(id=class_level_id)
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": "Class level with the provided ID does not exist."
        })

    # Build new value
    new_name = name.strip() if name is not None else level.name

    # Validate empty name
    if not new_name:
        raise ValidationError({
            "name": "Class level name cannot be empty."
        })

    # Validate duplicate
    if ClassLevel.objects.filter(
        school=level.school,
        name__iexact=new_name,
    ).exclude(
        id=level.id,
    ).exists():
        raise ValidationError({
            "name": "A class level with this name already exists for this school."
        })

    # Assign value
    if name is not None:
        level.name = new_name
        level.save()

    return level


# -------- Class Arm --------

@transaction.atomic
def create_class_arm(
    *,
    class_level_id: str,
    name: str,
) -> ClassArm:
    # Validate class level exists
    try:
        level = ClassLevel.objects.get(id=class_level_id)
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": "Class level with the provided ID does not exist."
        })

    # Clean name
    name = name.strip()

    # Validate empty name
    if not name:
        raise ValidationError({
            "name": "Class arm name cannot be empty."
        })

    # Validate duplicate
    if ClassArm.objects.filter(
        level=level,
        name__iexact=name,
    ).exists():
        raise ValidationError({
            "name": "A class arm with this name already exists for this class level."
        })

    # Create class arm
    arm = ClassArm(
        level=level,
        name=name,
    )

    arm.save()

    return arm


@transaction.atomic
def update_class_arm(
    *,
    class_arm_id: str,
    name: str | None = None,
) -> ClassArm:
    # Validate class arm exists
    try:
        arm = ClassArm.objects.get(id=class_arm_id)
    except ClassArm.DoesNotExist:
        raise ValidationError({
            "class_arm_id": "Class arm with the provided ID does not exist."
        })

    # Build new value
    new_name = name.strip() if name is not None else arm.name

    # Validate empty name
    if not new_name:
        raise ValidationError({
            "name": "Class arm name cannot be empty."
        })

    # Validate duplicate
    if ClassArm.objects.filter(
        level=arm.level,
        name__iexact=new_name,
    ).exclude(
        id=arm.id,
    ).exists():
        raise ValidationError({
            "name": "A class arm with this name already exists for this class level."
        })

    # Assign value
    arm.name = new_name

    arm.save()

    return arm