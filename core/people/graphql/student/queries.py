import strawberry

from people.graphql.permissions import (
    CanViewStudents,
)
from people.graphql.student.types import StudentType
from people.selectors.student_selectors import (
    get_student_by_id,
    get_student_by_name,
    get_student_by_admission_number,
    list_students,
    list_active_students,
    list_inactive_students,
)


@strawberry.type
class StudentQuery:

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def student(
        self,
        id: strawberry.ID,
    ) -> StudentType | None:
        return get_student_by_id(id)

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def student_by_name(
        self,
        school_id: strawberry.ID,
        first_name: str,
        last_name: str,
    ) -> StudentType | None:
        return get_student_by_name(
            school_id,
            first_name,
            last_name,
        )

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def student_by_admission_number(
        self,
        school_id: strawberry.ID,
        admission_number: str,
    ) -> StudentType | None:
        return get_student_by_admission_number(
            school_id,
            admission_number,
        )

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def students(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentType]:
        return list_students(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def active_students(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentType]:
        return list_active_students(
            school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudents],
    )
    def inactive_students(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentType]:
        return list_inactive_students(
            school_id,
            offset=offset,
            limit=limit,
        )