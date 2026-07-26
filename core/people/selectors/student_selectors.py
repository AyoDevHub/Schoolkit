from people.models import Student


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_student_by_id(
    student_id: str,
) -> Student | None:
    return Student.objects.filter(
        id=student_id,
    ).first()


def get_student_by_admission_number(
    school_id: str,
    admission_number: str,
) -> Student | None:
    return Student.objects.filter(
        school_id=school_id,
        admission_number__iexact=admission_number,
    ).first()


def get_student_by_name(
    school_id: str,
    first_name: str,
    last_name: str,
) -> Student | None:
    return Student.objects.filter(
        school_id=school_id,
        first_name__iexact=first_name,
        last_name__iexact=last_name,
    ).first()


def list_students(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Student.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_active_students(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Student.objects.filter(
        school_id=school_id,
        is_active=True,
    )[offset:offset + limit]


def list_inactive_students(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Student.objects.filter(
        school_id=school_id,
        is_active=False,
    )[offset:offset + limit]
