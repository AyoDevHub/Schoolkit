from people.models import Guardian


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_guardian_by_id(
    guardian_id: str,
) -> Guardian | None:
    return Guardian.objects.filter(
        id=guardian_id,
    ).first()


def get_guardian_by_phone_number(
    school_id: str,
    phone_number: str,
) -> Guardian | None:
    return Guardian.objects.filter(
        school_id=school_id,
        phone_number=phone_number,
    ).first()


def get_guardian_by_email(
    school_id: str,
    email: str,
) -> Guardian | None:
    return Guardian.objects.filter(
        school_id=school_id,
        email__iexact=email,
    ).first()


def get_guardian_by_name(
    school_id: str,
    first_name: str,
    last_name: str,
) -> Guardian | None:
    return Guardian.objects.filter(
        school_id=school_id,
        first_name__iexact=first_name,
        last_name__iexact=last_name,
    ).first()


def list_guardians(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Guardian.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_active_guardians(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Guardian.objects.filter(
        school_id=school_id,
        is_active=True,
    )[offset:offset + limit]


def list_inactive_guardians(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(offset, limit)

    return Guardian.objects.filter(
        school_id=school_id,
        is_active=False,
    )[offset:offset + limit]