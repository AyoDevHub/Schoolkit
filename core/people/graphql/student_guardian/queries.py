import strawberry

from people.graphql.permissions import (
    CanViewStudentGuardians,
)
from people.graphql.student_guardian.types import (
    StudentGuardianType,
)
from people.selectors.student_guardian_selectors import (
    get_student_guardian_by_id,
    list_active_student_guardians,
    list_guardians_for_student,
    list_inactive_student_guardians,
    list_student_guardians,
    list_students_for_guardian,
)


@strawberry.type
class StudentGuardianQuery:

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def student_guardian(
        self,
        id: strawberry.ID,
    ) -> StudentGuardianType | None:
        return get_student_guardian_by_id(id)

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def student_guardians(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentGuardianType]:
        return list_student_guardians(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def active_student_guardians(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentGuardianType]:
        return list_active_student_guardians(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def inactive_student_guardians(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentGuardianType]:
        return list_inactive_student_guardians(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def guardians_for_student(
        self,
        student_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentGuardianType]:
        return list_guardians_for_student(
            student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewStudentGuardians],
    )
    def students_for_guardian(
        self,
        guardian_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[StudentGuardianType]:
        return list_students_for_guardian(
            guardian_id,
            offset=offset,
            limit=limit,
        )