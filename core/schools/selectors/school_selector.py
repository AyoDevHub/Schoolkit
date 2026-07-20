from django.db.models import QuerySet 
from schools.models import School

def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit  = min(max(limit, 1), 100)
    return offset, limit

def get_school_by_id(school_id: str) -> School | None:
    return School.objects.filter(id=school_id).first()


def get_school_by_name(name: str) -> School | None:
    return School.objects.filter(name__iexact=name).first()


def get_school_by_code(code: str) -> School | None:
    return School.objects.filter(code__iexact=code).first()


def list_schools(offset: int = 0, limit: int = 20) -> QuerySet[School]:
    offset, limit = _paginate(offset, limit)
    return School.objects.all()[offset:offset + limit]


def list_active_schools(offset: int = 0, limit: int = 20) -> QuerySet[School]:
    offset, limit = _paginate(offset, limit)
    return School.objects.filter(is_active=True)[offset:offset + limit]


def list_inactive_schools(offset: int = 0, limit: int = 20) -> QuerySet[School]:
    offset, limit = _paginate(offset, limit)
    return School.objects.filter(is_active=False)[offset:offset + limit]