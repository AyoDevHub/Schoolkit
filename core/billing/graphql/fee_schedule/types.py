import strawberry
import strawberry_django

from billing.models import FeeSchedule


@strawberry_django.type(FeeSchedule)
class FeeScheduleType:
    id: strawberry.auto
    school: strawberry.auto
    academic_session: strawberry.auto
    academic_term: strawberry.auto
    class_level: strawberry.auto
    is_active: strawberry.auto
    due_date: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto