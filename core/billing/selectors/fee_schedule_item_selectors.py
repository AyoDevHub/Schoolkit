from decimal import Decimal

from django.db.models import Sum

from billing.models import FeeScheduleItem


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_fee_schedule_item_by_id(
    fee_schedule_item_id: str,
) -> FeeScheduleItem:
    return FeeScheduleItem.objects.get(
        id=fee_schedule_item_id,
    )


def list_fee_schedule_items_by_fee_schedule(
    fee_schedule_id: str,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    return FeeScheduleItem.objects.filter(
        fee_schedule_id=fee_schedule_id,
    )[offset:offset + limit]


def calculate_fee_schedule_total(
    fee_schedule_id: str,
) -> Decimal:
    total = FeeScheduleItem.objects.filter(
        fee_schedule_id=fee_schedule_id,
    ).aggregate(
        total=Sum("amount"),
    )["total"]

    return total or Decimal("0.00")