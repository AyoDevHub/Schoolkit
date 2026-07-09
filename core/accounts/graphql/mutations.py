import strawberry

from accounts.graphql.inputs import (
    CreateUserInput,
    UpdateUserInput,
    AssignSchoolInput,
    AssignRoleInput,
    ActivateUserInput,
    DeactivateUserInput,
    ChangePasswordInput,
    LoginInput,
    LogoutInput,
)
from accounts.services.user_services import (
    create_user as create_user_service,  
    update_user as update_user_service,
    assign_school as assign_school_service,
    assign_role as assign_role_service,
    activate_user as activate_user_service,
    deactivate_user as deactivate_user_service,
)
from accounts.services.auth_services import (
    change_password as change_password_service,
    login as login_service,
    logout as logout_service
)
from accounts.graphql.types import AdminUserType, LoginPayload, SuccessPayload
from strawberry.types import Info
from accounts.graphql.permissions import IsAuthenticated, CanAssignRoles,CanManageUsers,CanAssignSchools


@strawberry.type
class UserMutation:
    
    @strawberry.mutation(
        permission_classes=[CanManageUsers]
    )
    def create_user(
        self,
        input: CreateUserInput,
    ) -> AdminUserType:
        return create_user_service(
            email=input.email,
            first_name=input.first_name,
            last_name=input.last_name,
            password=input.password,
            role=input.role,
            school_id=input.school_id,
            phone_number=input.phone_number,
            home_address=input.home_address,
        )
        
        
    @strawberry.mutation(
        permission_classes=[CanManageUsers]
    )
    def update_user(
        self,
        input: UpdateUserInput,
    ) -> AdminUserType:
        return update_user_service(
            user_id=input.user_id,
            email=input.email,
            first_name=input.first_name,
            last_name=input.last_name,
            phone_number=input.phone_number,
            home_address=input.home_address,
        )
        
    
    @strawberry.mutation(
        permission_classes=[CanAssignSchools]
    )
    def assign_school(
        self,
        input: AssignSchoolInput,
    ) -> AdminUserType:
        return assign_school_service(
            user_id=input.user_id,
            school_id=input.school_id,
        )
        
        
    @strawberry.mutation(
        permission_classes=[CanAssignRoles]
    )
    def assign_role(
        self,
        input: AssignRoleInput,
    ) -> AdminUserType:
        return assign_role_service(
            user_id= input.user_id,
            role= input.role.value
        )


    @strawberry.mutation(
        permission_classes=[CanManageUsers]
    )
    def activate_user(
        self,
        input: ActivateUserInput,
    ) -> AdminUserType:
        return activate_user_service(
            user_id=input.user_id,
        )
        
        
    @strawberry.mutation(
        permission_classes=[CanManageUsers]
    )
    def deactivate_user(
        self,
        input: DeactivateUserInput,
    ) -> AdminUserType:
        return deactivate_user_service(
            user_id=input.user_id,
        )
        
        
        
    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    def change_password(
        self,
        info: Info,
        input: ChangePasswordInput
    ) -> SuccessPayload:
        
            change_password_service(
                user=info.context.user,
                old_password=input.old_password,
                new_password=input.new_password
            )
            
            return SuccessPayload(
                success=True,
                message="Password changed successfully."
            )
            
        
        
        
        
    @strawberry.mutation
    def login(
        self,
        input: LoginInput,
    ) -> LoginPayload:
        
        data= login_service(
            email=input.email,
            password=input.password
        )
        
        # Converting into Graphql type
        return LoginPayload(
            user=data["user"],
            accessToken=data["tokens"]["access_token"],
            refreshToken=data["tokens"]["refresh_token"],
        )
        
    
    @strawberry.mutation(
        permission_classes=[IsAuthenticated]
    )
    def logout(
        self,
        info: Info,
        input: LogoutInput
    ) -> SuccessPayload:
        
        logout_service(
            user=info.context.user,
            refresh_token=input.refresh_token
        )
        
        return SuccessPayload(
            success=True,
            message="Logged out successfully."
        )

    