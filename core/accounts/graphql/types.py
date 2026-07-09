import strawberry
import strawberry_django

from accounts.models import User


@strawberry_django.type(User)
class UserType:
    id: strawberry.auto
    email: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    role: strawberry.auto
    school: strawberry.auto
    home_address: strawberry.auto
    phone_number: strawberry.auto
    
    @strawberry.field(name="fullName")
    def get_full_name(self) -> str:
        return self.full_name 
    
    
    
@strawberry_django.type(User)
class AdminUserType:
    id: strawberry.auto
    email: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    role: strawberry.auto
    school: strawberry.auto
    phone_number: strawberry.auto
    home_address: strawberry.auto
    is_active: strawberry.auto
    last_login: strawberry.auto
    
    @strawberry.field(name="fullName")
    def get_full_name(self) -> str:
        return self.full_name
    

@strawberry.type
class LoginPayload:
    accessToken: str
    refreshToken: str
    user: UserType
    

@strawberry.type 
class SuccessPayload:
    success: bool
    message: str