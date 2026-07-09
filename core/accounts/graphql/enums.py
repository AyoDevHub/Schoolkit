import strawberry

from accounts.models import Role


RoleEnum = strawberry.enum(Role)