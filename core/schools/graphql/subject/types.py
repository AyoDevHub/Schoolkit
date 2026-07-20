import strawberry
import strawberry_django

from schools.models import Subject
from schools.graphql.school_class.types import ClassLevelType


@strawberry_django.type(Subject)
class SubjectType:
    id: strawberry.auto
    school: strawberry.auto
    name: strawberry.auto
    levels: list[ClassLevelType]
    created_at: strawberry.auto
    updated_at: strawberry.auto