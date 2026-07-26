import strawberry

from people.graphql.permissions import (
    CanActivateStudent,
    CanCreateStudent,
    CanDeactivateStudent,
    CanUpdateStudent,
)
from people.graphql.student.inputs import (
    ActivateStudentInput,
    CreateStudentInput,
    DeactivateStudentInput,
    UpdateStudentInput,
)
from people.graphql.student.types import StudentType
from people.services.student_services import (
    activate_student as activate_student_service,
    create_student as create_student_service,
    deactivate_student as deactivate_student_service,
    update_student as update_student_service,
)


@strawberry.type
class StudentMutation:

    @strawberry.mutation(
        permission_classes=[CanCreateStudent],
    )
    def create_student(
        self,
        input: CreateStudentInput,
    ) -> StudentType:
        return create_student_service(
            school_id=input.school_id,
            admission_number=input.admission_number,
            first_name=input.first_name,
            last_name=input.last_name,
            middle_name=input.middle_name,
            gender=input.gender,
            date_of_birth=input.date_of_birth,
            admission_date=input.admission_date,
        )

    @strawberry.mutation(
        permission_classes=[CanUpdateStudent],
    )
    def update_student(
        self,
        input: UpdateStudentInput,
    ) -> StudentType:
        return update_student_service(
            student_id=input.student_id,
            admission_number=input.admission_number,
            first_name=input.first_name,
            last_name=input.last_name,
            middle_name=input.middle_name,
            gender=input.gender,
            date_of_birth=input.date_of_birth,
            admission_date=input.admission_date,
        )

    @strawberry.mutation(
        permission_classes=[CanActivateStudent],
    )
    def activate_student(
        self,
        input: ActivateStudentInput,
    ) -> StudentType:
        return activate_student_service(
            student_id=input.student_id,
        )

    @strawberry.mutation(
        permission_classes=[CanDeactivateStudent],
    )
    def deactivate_student(
        self,
        input: DeactivateStudentInput,
    ) -> StudentType:
        return deactivate_student_service(
            student_id=input.student_id,
        )