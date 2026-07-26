import strawberry
import strawberry_django

from people.models import StudentGuardian
from people.graphql.student_guardian.enums import RelationshipTypeEnum

@strawberry_django.type(StudentGuardian)
class StudentGuardianType:
    id: strawberry.auto
    student: strawberry.auto
    guardian: strawberry.auto
    relationship: RelationshipTypeEnum
    is_primary: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto