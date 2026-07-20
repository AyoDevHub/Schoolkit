from django.db.models import QuerySet

from schools.models import AcademicTerm


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_term_by_id(term_id: str) -> AcademicTerm | None:
    return AcademicTerm.objects.filter(id=term_id).first()


def get_term_by_name(
    session_id: str,
    name: str,
) -> AcademicTerm | None:
    return AcademicTerm.objects.filter(
        session_id=session_id,
        name=name,
    ).first()


def list_terms(
    session_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicTerm]:
    offset, limit = _paginate(offset, limit)

    return AcademicTerm.objects.filter(
        session_id=session_id,
    ).order_by("start_date")[offset:offset + limit]


def list_current_terms(
    session_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicTerm]:
    offset, limit = _paginate(offset, limit)

    return AcademicTerm.objects.filter(
        session_id=session_id,
        is_current=True,
    ).orderby("start_date")[offset:offset + limit]


def list_inactive_terms(
    session_id: str,
    offset: int = 0,
    limit: int = 20,
) -> QuerySet[AcademicTerm]:
    offset, limit = _paginate(offset, limit)

    return AcademicTerm.objects.filter(
        session_id=session_id,
        is_current=False,
    ).order_by("start_date")[offset:offset + limit]