import strawberry
import strawberry_django

from schools.models import AcademicSession


@strawberry_django.type(AcademicSession)
class AcademicSessionType:
    id: strawberry.auto
    school: strawberry.auto
    name: strawberry.auto
    start_date: strawberry.auto
    end_date: strawberry.auto
    is_current: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto