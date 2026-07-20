from django.db.models import QuerySet

from schools.models import AcademicSession


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_session_by_id(session_id: str) -> AcademicSession | None:
    return AcademicSession.objects.filter(id=session_id).first()


def get_session_by_name(
    school_id: str,
    name: str,
) -> AcademicSession | None:
    return AcademicSession.objects.filter(
        school_id=school_id,
        name__iexact=name,
    ).first()


def list_sessions(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicSession]:
    offset, limit = _paginate(offset, limit)

    return AcademicSession.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_current_sessions(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicSession]:
    offset, limit = _paginate(offset, limit)

    return AcademicSession.objects.filter(
        school_id=school_id,
        is_current=True,
    )[offset:offset + limit]


def list_inactive_sessions(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicSession]:
    offset, limit = _paginate(offset, limit)

    return AcademicSession.objects.filter(
        school_id=school_id,
        is_current=False,
    )[offset:offset + limit]