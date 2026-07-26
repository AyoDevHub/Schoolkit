import strawberry
import strawberry_django

from people.models import Enrollment
from people.graphql.enrollment.enums import EnrollmentStatusEnum


@strawberry_django.type(Enrollment)
class EnrollmentType:
    id: strawberry.auto
    school: strawberry.auto
    student: strawberry.auto
    academic_session: strawberry.auto
    academic_term: strawberry.auto
    class_level: strawberry.auto
    class_arm: strawberry.auto
    status: EnrollmentStatusEnum
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto