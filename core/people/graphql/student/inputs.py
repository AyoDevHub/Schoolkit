import strawberry

from people.graphql.student.enums import GenderEnum


@strawberry.input
class CreateStudentInput:
    school_id: strawberry.ID
    admission_number: str
    first_name: str
    last_name: str
    middle_name: str = ""
    gender: GenderEnum
    date_of_birth: str
    admission_date: str


@strawberry.input
class UpdateStudentInput:
    student_id: strawberry.ID
    admission_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    gender: GenderEnum | None = None
    date_of_birth: str | None = None
    admission_date: str | None = None


@strawberry.input
class ActivateStudentInput:
    student_id: strawberry.ID


@strawberry.input
class DeactivateStudentInput:
    student_id: strawberry.ID