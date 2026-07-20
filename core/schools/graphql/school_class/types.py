import strawberry
import strawberry_django

from schools.models import ClassLevel, ClassArm

# -------- Class Level --------

@strawberry_django.type(ClassLevel)
class ClassLevelType:
    id: strawberry.auto
    school: strawberry.auto
    name: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto


# -------- Class Arm --------

@strawberry_django.type(ClassArm)
class ClassArmType:
    id: strawberry.auto
    level: strawberry.auto
    name: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

