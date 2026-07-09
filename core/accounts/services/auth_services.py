from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@transaction.atomic
def change_password(
    *,
    user:User,
    old_password: str,
    new_password: str,
) -> User:
    # Check if the old password is correct
    if not user.check_password(old_password):
        raise ValidationError({
            "old_password":
                "The current password is incorrect!"
                })
    
    
    # Preventing password reuse 
    if old_password == new_password:
        raise ValidationError({
            "new_password":
                "New password must be different from the old password!"
                })
        

    # Validating the password
    validate_password(new_password, user=user)

    # Set the new password
    user.set_password(new_password)
    
    user.save()
    
    return user
    


def reset_password():
    pass



def login(
    *,
    email: str,
    password: str
) -> dict[str, object]:
    # Authenticate the user 
    user = authenticate(
        email=email,
        password=password,
    )
    
    if user is None:
        raise ValidationError(
            {
                "credentials":"Invalid email or password!"
            }
        )
        
    # Generating the tokens 
    refresh= RefreshToken.for_user(user)
    access= refresh.access_token
    
    
    return {
        "user": user,
        "tokens" : {
            "refresh_token": str(refresh),
            "access_token": str(access),
        }
    }
    
    

def logout(
    *, 
    user: User,
    refresh_token: str
) -> None:
    
    try:
        token = RefreshToken(refresh_token)

    except TokenError:
        raise ValidationError({
            "refresh_token": "Invalid or expired refresh token."
        })
     
        
    token_user_id = token["user_id"]
  
  
    if token_user_id!= str(user.id):
        raise PermissionDenied(
            "You cannot revoke another user's session."
        ) 
    
    token.blacklist()
