from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from schools.models import School
from accounts.models import Role


User = get_user_model()


@transaction.atomic
def create_user(
    *,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    role: Role,
    school_id: str | None = None,
    phone_number: str = "",
    home_address: str,
) -> User:
    
    # Validate the email format
    try: 
        validate_email(email)
        
    except ValidationError:
        raise ValidationError({"email": "Enter a valid email address."})
    
    
    # Validate the email and password
    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError(
            {"email": "A user with this email already exists."}
        )
        
        
    validate_password(password)


    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=role,
        school_id=school_id,
        phone_number=phone_number,
        home_address=home_address,
    )


    user.set_password(password)

    user.save()

    return user



@transaction.atomic
def update_user(
    *,
    user_id: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    phone_number: str | None = None,
    home_address: str | None = None,
) -> User:
    
    try:
        user = User.objects.get(id=user_id)
        
    except User.DoesNotExist:
        raise ValidationError({"user_id": "User does not exist."})
    
    
    
    # Update user information
    if email is not None:
        # Validate the email format
        try:
            validate_email(email)
            
        except ValidationError:
            raise ValidationError({"email": "Enter a valid email address."})
        
        
        # Validating the email to ensure uniqueness before assigning
        if User.objects.filter(email__iexact=email).exclude(id=user.id).exists():
            raise ValidationError(
                {"email": "A user with this email already exists."}
            )
        
        user.email = email
            
            
    if first_name is not None:
        user.first_name = first_name
        
        
    if last_name is not None:
        user.last_name = last_name
        
        
    if phone_number is not None:
        user.phone_number = phone_number
        
        
    if home_address is not None:
        user.home_address = home_address


    user.save()

    return user
    
    
@transaction.atomic
def activate_user(
    *,
    user_id: str
) -> User:
    try:
        user = User.objects.get(id=user_id)
        
    except User.DoesNotExist:
        raise ValidationError({"user_id": "User does not exist."})
    
    if user.is_active:
        return user 
    
    
    user.is_active = True
    
    user.save()
    
    return user


@transaction.atomic
def deactivate_user(
    *,
    user_id: str
) -> User:
    try:
        user = User.objects.get(id=user_id)
        
    except User.DoesNotExist:
        raise ValidationError({"user_id": "User does not exist."})
    
    
    if not user.is_active:
        return user 
    
    user.is_active = False
    
    user.save()
    
    return user



@transaction.atomic
def assign_role(
    *,
    user_id: str,
    role: Role 
) -> User:
    
    try:
        user = User.objects.get(id=user_id)
        
    except User.DoesNotExist:
        raise ValidationError({"user_id": "User does not exist."})
    

    if user.role == role:
        return user 
    
    # Check if the user belongs to a school before assigning certain roles
    if role in (
        Role.BURSAR,
        Role.TEACHER,
    ) and user.school is None:
        raise ValidationError(
            {"school_id": "User must belong to a school before being assigned this role."}
        )
        
        
    user.role = role 
    
    user.save()
    
    return user 
    

@transaction.atomic
def assign_school(
    *,
    user_id: str,
    school_id: str
) -> User:
    try:
        user = User.objects.get(id=user_id)
        school = School.objects.get(id=school_id)
    except User.DoesNotExist:
        raise ValidationError({"user_id": "User does not exist."})
    except School.DoesNotExist:
        raise ValidationError({"school_id": "School does not exist."})


    if user.school == school:
        return user
    
    user.school = school
    
    user.save()
    
    return user 
    
    