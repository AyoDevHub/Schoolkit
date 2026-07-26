from people.models import StudentGuardian


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_student_guardian_by_id(
    student_guardian_id: str,
) -> StudentGuardian | None:
    return StudentGuardian.objects.filter(
        id=student_guardian_id,
    ).first()


def list_student_guardians(
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return StudentGuardian.objects.all()[
        offset:offset + limit
    ]


def list_active_student_guardians(
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return StudentGuardian.objects.filter(
        is_active=True,
    )[offset:offset + limit]


def list_inactive_student_guardians(
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return StudentGuardian.objects.filter(
        is_active=False,
    )[offset:offset + limit]


def list_guardians_for_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return StudentGuardian.objects.filter(
        student_id=student_id,
        is_active=True,
    ).order_by(
        "-is_primary",
        "guardian__last_name",
        "guardian__first_name",
    )[offset:offset + limit]


def list_students_for_guardian(
    guardian_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return StudentGuardian.objects.filter(
        guardian_id=guardian_id,
        is_active=True,
    ).order_by(
        "student__last_name",
        "student__first_name",
    )[offset:offset + limit]