from billing.models import FeeItem



def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_fee_item_by_id(
    fee_item_id: str,
) -> FeeItem:
    return FeeItem.objects.get(
        id=fee_item_id,
    )


def list_fee_items(
    school_id: str,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    return FeeItem.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_active_fee_items(
    school_id: str,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    return FeeItem.objects.filter(
        school_id=school_id,
        is_active=True,
    )[offset:offset + limit]


def list_inactive_fee_items(
    school_id: str,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    return FeeItem.objects.filter(
        school_id=school_id,
        is_active=False,
    )[offset:offset + limit]