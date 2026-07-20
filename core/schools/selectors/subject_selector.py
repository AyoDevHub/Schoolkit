from schools.models import Subject


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_subject_by_id(
    subject_id: str,
) -> Subject | None:
    return Subject.objects.filter(
        id=subject_id,
    ).first()


def get_subject_by_name(
    school_id: str,
    name: str,
) -> Subject | None:
    return Subject.objects.filter(
        school_id=school_id,
        name__iexact=name,
    ).first()


def list_subjects(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Subject.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]