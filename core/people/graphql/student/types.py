import strawberry
import strawberry_django

from people.models import Student
from people.graphql.student.enums import GenderEnum

@strawberry_django.type(Student)
class StudentType:
    id: strawberry.auto
    school: strawberry.auto
    admission_number: strawberry.auto
    first_name: strawberry.auto
    last_name: strawberry.auto
    middle_name: strawberry.auto
    gender: GenderEnum
    date_of_birth: strawberry.auto
    admission_date: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

    @strawberry.field(name="fullName")
    def get_full_name(self) -> str:
        return self.full_name 
    