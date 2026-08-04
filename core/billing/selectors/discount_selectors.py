from billing.models import Discount


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_discount_by_id(
    discount_id: str,
) -> Discount:
    return Discount.objects.get(
        id=discount_id,
    )


def list_discounts(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Discount.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_active_discounts(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Discount.objects.filter(
        school_id=school_id,
        is_active=True,
    )[offset:offset + limit]


def list_inactive_discounts(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Discount.objects.filter(
        school_id=school_id,
        is_active=False,
    )[offset:offset + limit]


def list_discounts_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Discount.objects.filter(
        student_id=student_id,
    )[offset:offset + limit]


def get_active_student_discounts(
    *,
    student_id: str,
    academic_session_id: str,
    academic_term_id: str,
    offset: int=0,
    limit: int= 20,
):

    offset, limit = _paginate(offset, limit)

    return Discount.objects.filter(
        student_id=student_id,
        academic_session_id=academic_session_id,
        academic_term_id=academic_term_id,
        is_active=True,
    )[offset:offset + limit]