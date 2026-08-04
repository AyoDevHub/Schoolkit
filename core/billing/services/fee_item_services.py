from django.core.exceptions import ValidationError
from django.db import transaction

from billing.models import FeeItem
from schools.models import School


@transaction.atomic
def create_fee_item(
    school_id: str,
    name: str,
    description: str = "",
    is_recurring: bool = True,
) -> FeeItem:
     # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })  
    
    # Clean input
    name = name.strip()
    description = description.strip()

    # Check for duplicates
    if FeeItem.objects.filter(
        school=school,
        name__iexact=name,
    ).exists():
        raise ValidationError({
           "name": "A fee item with this name already exists."
        })

    # Create fee_item 
    fee_item = FeeItem(
        school=school,
        name=name,
        description=description,
        is_recurring=is_recurring,
    )

    fee_item.save()
    return fee_item


@transaction.atomic
def update_fee_item(
    fee_item_id: str,
    name: str | None = None ,
    description: str | None = None,
    is_recurring: bool | None = None,
) -> FeeItem:  
    # Validate fee_item exists
    try:
        fee_item = FeeItem.objects.get(id=fee_item_id)
    except FeeItem.DoesNotExist:
        raise ValidationError({
            "fee_item_id": "FeeItem with the provided ID does not exist."
        })

    # Build new values 
    new_name = (
        name.strip()
        if name is not None
        else fee_item.name
    )

    new_description = description.strip() if description is not None else fee_item.description
    new_is_recurring = (
        is_recurring
        if is_recurring is not None
        else fee_item.is_recurring
    )

    if not name:
        raise ValidationError({
            "name": "Name cannot be empty."
        })

    # Check for duplicates
    if (
        fee_item.name.lower() != new_name.lower()
        and FeeItem.objects.filter(
            school=fee_item.school,
            name__iexact=new_name,
        ).exclude(
            id=fee_item.id
        ).exists()
    ):
        raise ValidationError({
            "name": "A fee item with this name already exists."
        })

    # Assign Values
    fee_item.name = new_name
    fee_item.description = new_description
    fee_item.is_recurring = new_is_recurring

    fee_item.save()

    return fee_item


@transaction.atomic
def activate_fee_item(
    fee_item_id: str,
) -> FeeItem:
    # Validate fee_item exists
    try:
        fee_item = FeeItem.objects.get(id=fee_item_id)
    except FeeItem.DoesNotExist:
        raise ValidationError({
            "fee_item_id": "FeeItem with the provided ID does not exist."
        })

    # Already active 
    if fee_item.is_active:
        return fee_item

    fee_item.is_active = True
    fee_item.save()

    return fee_item


@transaction.atomic
def deactivate_fee_item(
    fee_item_id: str,
) -> FeeItem:
    # Validate fee_item exists
    try:
        fee_item = FeeItem.objects.get(id=fee_item_id)
    except FeeItem.DoesNotExist:
        raise ValidationError({
            "fee_item_id": "FeeItem with the provided ID does not exist."
        })

    # Already inactive 
    if not fee_item.is_active:
        return fee_item

    fee_item.is_active = False
    fee_item.save()

    return fee_item