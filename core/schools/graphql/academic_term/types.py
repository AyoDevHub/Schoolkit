import strawberry
import strawberry_django

from schools.models import AcademicTerm


@strawberry_django.type(AcademicTerm)
class AcademicTermType:
    id: strawberry.auto
    session: strawberry.auto
    name: strawberry.auto
    start_date: strawberry.auto
    end_date: strawberry.auto
    is_current: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto