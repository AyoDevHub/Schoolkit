from billing.models import FeeSchedule


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_fee_schedule_by_id(
    fee_schedule_id: str,
) -> FeeSchedule:
    return FeeSchedule.objects.get(
        id=fee_schedule_id,
    )


def list_fee_schedules(
    school_id: str,
    academic_session_id: str | None = None,
    academic_term_id: str | None = None,
    class_level_id: str | None = None,
    is_active: bool | None = None,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    queryset = FeeSchedule.objects.filter(
        school_id=school_id,
    )

    if academic_session_id is not None:
        queryset = queryset.filter(
            academic_session_id=academic_session_id,
        )

    if academic_term_id is not None:
        queryset = queryset.filter(
            academic_term_id=academic_term_id,
        )

    if class_level_id is not None:
        queryset = queryset.filter(
            class_level_id=class_level_id,
        )

    if is_active is not None:
        queryset = queryset.filter(
            is_active=is_active,
        )

    return queryset[
        offset:offset + limit
    ]