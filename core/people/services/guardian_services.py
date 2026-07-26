from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from people.models import Guardian, Title
from schools.models import School


@transaction.atomic
def create_guardian(
    *,
    school_id: str,
    title: str = "",
    first_name: str,
    last_name: str,
    middle_name: str = "",
    phone_number: str,
    email: str = "",
    home_address: str = "",
    receive_sms: bool = True,
    receive_email: bool = True,
) -> Guardian:

    # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })


    # Clean input
    title = title.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    middle_name = middle_name.strip()
    phone_number = phone_number.strip()
    email = email.strip()
    home_address = home_address.strip()

    # Validate the email
    if email:
         try:
             validate_email(email)
         except ValidationError:
             raise ValidationError({
                "email": "Enter a valid email address."
            })

    # Validate required fields
    if not first_name:
        raise ValidationError({
            "first_name": "First name cannot be empty."
        })

    if not last_name:
        raise ValidationError({
            "last_name": "Last name cannot be empty."
        })

    if not phone_number:
        raise ValidationError({
            "phone_number": "Phone number cannot be empty."
        })

    # Validate duplicate phone number
    if Guardian.objects.filter(
        school=school,
        phone_number=phone_number,
    ).exists():
        raise ValidationError({
            "phone_number": (
                "A guardian with this phone number already exists for this school."
            )
        })

    
    # Validate phone number
    if not phone_number.isdigit():
        raise ValidationError({
            "phone_number": "Phone number must contain only digits."
        })

    if len(phone_number) < 11 or len(phone_number) > 15:
        raise ValidationError({
            "phone_number": (
                "Phone number must be between 11 and 15 digits."
            )
        })

    # Create guardian
    guardian = Guardian(
        school=school,
        title=title,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone_number=phone_number,
        email=email,
        home_address=home_address,
        receive_sms=receive_sms,
        receive_email=receive_email,
    )

    guardian.save()

    return guardian



@transaction.atomic
def update_guardian(
    *,
    guardian_id: str,
    title: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    middle_name: str | None = None,
    phone_number: str | None = None,
    email: str | None = None,
    home_address: str | None = None,
    receive_sms: bool | None = None,
    receive_email: bool | None = None,
) -> Guardian:

    # Validate guardian exists
    try:
        guardian = Guardian.objects.get(id=guardian_id)
    except Guardian.DoesNotExist:
        raise ValidationError({
            "guardian_id": "Guardian with the provided ID does not exist."
        })

    # Build new values
    new_title = title.strip() if title is not None else guardian.title
    new_first_name = (
        first_name.strip()
        if first_name is not None
        else guardian.first_name
    )
    new_last_name = (
        last_name.strip()
        if last_name is not None
        else guardian.last_name
    )
    new_middle_name = (
        middle_name.strip()
        if middle_name is not None
        else guardian.middle_name
    )
    new_phone_number = (
        phone_number.strip()
        if phone_number is not None
        else guardian.phone_number
    )
    new_email = (
        email.strip()
        if email is not None
        else guardian.email
    )
    new_home_address = (
        home_address.strip()
        if home_address is not None
        else guardian.home_address
    )

    new_receive_sms = (
        receive_sms
        if receive_sms is not None
        else guardian.receive_sms
    )

    new_receive_email = (
        receive_email
        if receive_email is not None
        else guardian.receive_email
    )

    # Validate required fields
    if not new_first_name:
        raise ValidationError({
            "first_name": "First name cannot be empty."
        })

    if not new_last_name:
        raise ValidationError({
            "last_name": "Last name cannot be empty."
        })

    if not new_phone_number:
        raise ValidationError({
            "phone_number": "Phone number cannot be empty."
        })

    # Validate email
    if new_email:
        try:
            validate_email(new_email)
        except ValidationError:
            raise ValidationError({
                "email": "Enter a valid email address."
            })

    # Validate phone number
    if not new_phone_number.isdigit():
        raise ValidationError({
            "phone_number": "Phone number must contain only digits."
        })

    if len(new_phone_number) < 11 or len(new_phone_number) > 15:
        raise ValidationError({
            "phone_number": (
                "Phone number must be between 11 and 15 digits."
            )
        })

    # Validate duplicate phone number
    if Guardian.objects.filter(
        school=guardian.school,
        phone_number=new_phone_number,
    ).exclude(
        id=guardian.id,
    ).exists():
        raise ValidationError({
            "phone_number": (
                "A guardian with this phone number already exists for this school."
            )
        })

    # Assign values
    guardian.title = new_title
    guardian.first_name = new_first_name
    guardian.last_name = new_last_name
    guardian.middle_name = new_middle_name
    guardian.phone_number = new_phone_number
    guardian.email = new_email
    guardian.home_address = new_home_address
    guardian.receive_sms = new_receive_sms
    guardian.receive_email = new_receive_email

    guardian.save()

    return guardian


@transaction.atomic
def activate_guardian(
    *,
    guardian_id: str,
) -> Guardian:

    try:
        guardian = Guardian.objects.get(id=guardian_id)
    except Guardian.DoesNotExist:
        raise ValidationError({
            "guardian_id": "Guardian with the provided ID does not exist."
        })

    if guardian.is_active:
        return guardian

    guardian.is_active = True
    guardian.save()

    return guardian


@transaction.atomic
def deactivate_guardian(
    *,
    guardian_id: str,
) -> Guardian:

    try:
        guardian = Guardian.objects.get(id=guardian_id)
    except Guardian.DoesNotExist:
        raise ValidationError({
            "guardian_id": "Guardian with the provided ID does not exist."
        })

    if not guardian.is_active:
        return guardian

    guardian.is_active = False
    guardian.save()

    return guardian