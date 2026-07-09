from strawberry.permission import BasePermission
from strawberry.types import Info

#Authentication 

class IsAuthenticated(BasePermission):
    
    # The Error message
    message = "Authentication required."
    
    def has_permission(self, source, info:Info,**kwargs) -> bool:
        return info.context.user is not None 
    
    

# User management

class CanManageUsers(BasePermission):
    message = "You do not have permission to manage users."

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        
        user = info.context.user

        if user is None:
            return False
        
        return user.is_administrator


class CanAssignRoles(BasePermission):
    
    message = "You do not have permission to assign roles."
    
    def has_permission(self, source, info:Info, **kwargs) -> bool:
        
        user = info.context.user
        
        if user is None:
            return False
        
        return user.is_administrator
    
    
class CanAssignSchools(BasePermission):
    
    message = "You do not have permission to assign school."
    
    def has_permission(self, source, info:Info, **kwargs) -> bool:
        
        user = info.context.user
        
        if user is None:
            return False
        
        return user.is_administrator
    
    

class CanViewUsers(BasePermission):
    
    message = "You do not have permission to view users."
    
    def has_permission(self, source, info:Info, **kwargs) -> bool:
        
        user = info.context.user
        
        if user is None:
            return False
        
        return user.is_administrator
    