from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.base_user import BaseUserManager
from schools.models import School


@transaction.atomic
def create_school(
    *,
    name: str,
    code: str,
    email: str,
    phone_number: str = "",
    address: str = "",
    website: str = "",
    motto: str = "",
    logo=None,
) -> School:
    # Validate email
    try:
        validate_email(email)

    except ValidationError:
        raise ValidationError({
            "email": "Enter a valid email address."
        })


    # Validate website
    if website:
        try:
            URLValidator()(website)

        except ValidationError:
            raise ValidationError({
                "website": "Enter a valid website URL."
            })


    # Ensure unique school name
    if School.objects.filter(name__iexact=name).exists():
        raise ValidationError({
            "name": "A school with this name already exists."
        })


    # Ensure unique school code
    if School.objects.filter(code__iexact=code).exists():
        raise ValidationError({
            "code": "A school with this code already exists."
        })


    # Ensure unique email
    if School.objects.filter(email__iexact=email).exists():
        raise ValidationError({
            "email": "A school with this email already exists."
        })


    school = School(
        name=name.strip(),
        code=code.strip(),
        email=email.strip(),
        phone_number=phone_number,
        address=address,
        website=website,
        motto=motto,
        logo=logo,
    )

    school.save()

    return school


@transaction.atomic
def update_school(
        *,
        school_id: str,
        name: str | None = None,
        code: str | None = None,
        email: str | None = None,
        phone_number: str | None = None,
        address: str | None = None,
        website: str | None = None,
        motto: str | None = None,
        logo=None,
) -> School:
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })
    
    # Update the fields if they are provided
    if name is not None:
        if School.objects.filter(name__iexact=name).exclude(id=school_id).exists():
            raise ValidationError({
                "name": "A school with this name already exists."
            })
        
        school.name = name.strip()
    
    if code is not None:
        if School.objects.filter(code__iexact=code).exclude(id=school_id).exists():
            raise ValidationError({
                "code": "A school with this code already exists."
            })
        
        school.code = code.strip()
    
    if email is not None:

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError({
                "email": "Enter a valid email address."
            })


        if School.objects.filter(email__iexact=email).exclude(id=school_id).exists():
            raise ValidationError({
                "email": "A school with this email already exists."
            })
        
        
        school.email = BaseUserManager.normalize_email(email.strip())

    if website is not None:
        try:
            URLValidator()(website)
        except ValidationError:
            raise ValidationError({
                "website": "Enter a valid website URL."
            })
        
        school.website = website.strip

    if phone_number is not None:
        school.phone_number = phone_number.strip()

    if address is not None:
        school.address = address.strip()

    if motto is not None:
        school.motto = motto.strip()

    if logo is not None:
        school.logo = logo

    school.save()

    return school


@transaction.atomic
def activate_school(
        *,
        school_id: str,
) -> School:
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })
    
    if school.is_active:
        return school
    
    school.is_active = True
    school.save()

    return school


@transaction.atomic
def deactivate_school(
        *,
        school_id: str,
) -> School:
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })
    
    if not school.is_active:
        return school
    
    school.is_active = False
    school.save()

    return school