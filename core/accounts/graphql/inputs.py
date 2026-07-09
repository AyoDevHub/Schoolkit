import strawberry

from accounts.graphql.enums import RoleEnum 

@strawberry.input
class CreateUserInput:
    email: str
    first_name: str
    last_name: str
    password: str
    role: RoleEnum 
    school_id: str | None = None
    phone_number: str = "" 
    home_address: str = ""
    

@strawberry.input
class UpdateUserInput:
    user_id: strawberry.ID
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    home_address: str | None = None
    

@strawberry.input
class AssignSchoolInput:
    user_id: strawberry.ID
    school_id: strawberry.ID
    

@strawberry.input
class AssignRoleInput:
    user_id: strawberry.ID
    role: RoleEnum
    

@strawberry.input
class ActivateUserInput:
    user_id: strawberry.ID  


@strawberry.input
class DeactivateUserInput:
    user_id: strawberry.ID  
    

@strawberry.input
class ChangePasswordInput:
    old_password: str
    new_password: str
    

@strawberry.input 
class LoginInput:
    email: str
    password: str 
    

@strawberry.input
class LogoutInput:
    refresh_token: str
    
