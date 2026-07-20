import strawberry
import strawberry_django

from schools.models import School

@strawberry_django.type(School)
class SchoolType:
    id : strawberry.auto
    name : strawberry.auto
    code : strawberry.auto
    email : strawberry.auto
    phone_number : strawberry.auto
    address : strawberry.auto
    website : strawberry.auto
    motto : strawberry.auto
    logo : strawberry.auto

 

@strawberry_django.type(School)
class AdminSchoolType:
    id : strawberry.auto
    name : strawberry.auto
    code : strawberry.auto
    email : strawberry.auto
    phone_number : strawberry.auto
    address : strawberry.auto
    website : strawberry.auto
    motto : strawberry.auto
    logo : strawberry.auto
    is_active : strawberry.auto
    created_at : strawberry.auto
    updated_at : strawberry.auto