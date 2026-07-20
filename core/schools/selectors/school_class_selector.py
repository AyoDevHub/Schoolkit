from schools.models import ClassLevel, ClassArm


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


# -------- Class Level --------

def get_class_level_by_id(
    class_level_id: str,
) -> ClassLevel | None:
    return ClassLevel.objects.filter(
        id=class_level_id,
    ).first()


def get_class_level_by_name(
    school_id: str,
    name: str,
) -> ClassLevel | None:
    return ClassLevel.objects.filter(
        school_id=school_id,
        name__iexact=name,
    ).first()


def list_class_levels(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return ClassLevel.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


# -------- Class Arm--------

def get_class_arm_by_id(
    class_arm_id: str,
) -> ClassArm | None:
    return ClassArm.objects.filter(
        id=class_arm_id,
    ).first()


def get_class_arm_by_name(
    class_level_id: str,
    name: str,
) -> ClassArm | None:
    return ClassArm.objects.filter(
        level_id=class_level_id,
        name__iexact=name,
    ).first()


def list_class_arms(
    class_level_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return ClassArm.objects.filter(
        level_id=class_level_id,
    )[offset:offset + limit]