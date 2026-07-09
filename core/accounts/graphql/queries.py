import strawberry

from accounts.graphql.enums import RoleEnum
from accounts.graphql.types import UserType, AdminUserType
from accounts.graphql.permissions import CanViewUsers
from accounts.selectors import (
    list_users, get_user_by_id, get_user_by_email, list_active_users, list_users_by_school, list_users_by_role, list_inactive_users, list_users_by_school_name
)



@strawberry.type()
class UserQuery:
    
    # Single User Queries     
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def user(self, 
             id: strawberry.ID
             ) -> AdminUserType | None:
        return get_user_by_id(id)


    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def user_by_email(self,
                      email: str
                      ) -> AdminUserType | None:
        return get_user_by_email(email)
    
    
    
    # Collection Queries
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def users(self,
              offset: int = 0, 
              limit: int = 20
              ) -> list[AdminUserType]:
        
        return list_users(offset=offset, limit=limit)
    
    
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def active_users(self,
                     offset: int = 0,
                     limit: int = 20
                     ) -> list[UserType]:
        return list_active_users(offset=offset, limit=limit)
    
    
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def inactive_users(self,
                       offset: int = 0,
                       limit: int = 20
                       ) -> list[UserType]:
        return list_inactive_users(offset=offset, limit=limit)  
    
    
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def users_by_school(self,
                        school_id: str,
                        offset: int = 0,
                        limit: int = 20
                        ) -> list[UserType]:
        return list_users_by_school(school_id=school_id, offset=offset, limit=limit)
    
    
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def users_by_school_name(self,
                          school_name: str,
                          offset: int = 0,
                          limit: int = 20
                          ) -> list[UserType]:
        return list_users_by_school_name(school_name=school_name, offset=offset, limit=limit)
    
    
    @strawberry.field(
        permission_classes=[CanViewUsers]
    )
    def users_by_role(self,
                      role: RoleEnum,
                      offset: int = 0,
                      limit: int = 20
                      ) -> list[AdminUserType]:
        return list_users_by_role(role=role, offset=offset, limit=limit)
    
