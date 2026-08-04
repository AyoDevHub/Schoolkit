from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from billing.models import (
    FeeItem,
    FeeSchedule,
    FeeScheduleItem,
)


@transaction.atomic
def create_fee_schedule_item(
    fee_schedule_id: str,
    fee_item_id: str,
    amount: Decimal,
) -> FeeScheduleItem:
    # Validate fee schedule exists
    try:
        fee_schedule = FeeSchedule.objects.get(
            id=fee_schedule_id,
        )
    except FeeSchedule.DoesNotExist:
        raise ValidationError({
            "fee_schedule_id":
                "Fee Schedule with the provided ID does not exist."
        })

    # Validate fee item exists
    try:
        fee_item = FeeItem.objects.get(
            id=fee_item_id,
        )
    except FeeItem.DoesNotExist:
        raise ValidationError({
            "fee_item_id":
                "Fee Item with the provided ID does not exist."
        })

    # Validate amount
    if amount <= 0:
        raise ValidationError({
            "amount":
                "Amount must be greater than zero."
        })

    # Check for duplicates
    if FeeScheduleItem.objects.filter(
        fee_schedule=fee_schedule,
        fee_item=fee_item,
    ).exists():
        raise ValidationError(
            "This fee item already exists in the selected fee schedule."
        )

    # Create fee schedule item
    fee_schedule_item = FeeScheduleItem(
        fee_schedule=fee_schedule,
        fee_item=fee_item,
        amount=amount,
    )

    fee_schedule_item.save()

    return fee_schedule_item


@transaction.atomic
def update_fee_schedule_item(
    fee_schedule_item_id: str,
    fee_item_id: str | None = None,
    amount: Decimal | None = None,
) -> FeeScheduleItem:
    # Validate fee schedule item exists
    try:
        fee_schedule_item = FeeScheduleItem.objects.get(
            id=fee_schedule_item_id,
        )
    except FeeScheduleItem.DoesNotExist:
        raise ValidationError({
            "fee_schedule_item_id":
                "Fee Schedule Item with the provided ID does not exist."
        })

    fee_item = fee_schedule_item.fee_item

    # Validate fee item
    if fee_item_id is not None:
        try:
            fee_item = FeeItem.objects.get(
                id=fee_item_id,
            )
        except FeeItem.DoesNotExist:
            raise ValidationError({
                "fee_item_id":
                    "Fee Item with the provided ID does not exist."
            })

    new_amount = (
        amount
        if amount is not None
        else fee_schedule_item.amount
    )

    # Validate amount
    if new_amount <= 0:
        raise ValidationError({
            "amount":
                "Amount must be greater than zero."
        })

    # Check for duplicates
    if FeeScheduleItem.objects.filter(
        fee_schedule=fee_schedule_item.fee_schedule,
        fee_item=fee_item,
    ).exclude(
        id=fee_schedule_item.id,
    ).exists():
        raise ValidationError(
            "This fee item already exists in the selected fee schedule."
        )

    # Assign values
    fee_schedule_item.fee_item = fee_item
    fee_schedule_item.amount = new_amount

    fee_schedule_item.save()

    return fee_schedule_item


@transaction.atomic
def delete_fee_schedule_item(
    fee_schedule_item_id: str,
) -> None:
    # Validate fee schedule item exists
    try:
        fee_schedule_item = FeeScheduleItem.objects.get(
            id=fee_schedule_item_id,
        )
    except FeeScheduleItem.DoesNotExist:
        raise ValidationError({
            "fee_schedule_item_id":
                "Fee Schedule Item with the provided ID does not exist."
        })

    fee_schedule_item.delete()