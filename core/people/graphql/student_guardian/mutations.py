import strawberry

from people.graphql.permissions import (
    CanActivateStudentGuardian,
    CanCreateStudentGuardian,
    CanDeactivateStudentGuardian,
    CanUpdateStudentGuardian,
)
from people.graphql.student_guardian.inputs import (
    ActivateStudentGuardianInput,
    CreateStudentGuardianInput,
    DeactivateStudentGuardianInput,
    UpdateStudentGuardianInput,
)
from people.graphql.student_guardian.types import (
    StudentGuardianType,
)
from people.services.student_guardian_services import (
    activate_student_guardian as activate_student_guardian_service,
    create_student_guardian as create_student_guardian_service,
    deactivate_student_guardian as deactivate_student_guardian_service,
    update_student_guardian as update_student_guardian_service,
)


@strawberry.type
class StudentGuardianMutation:

    @strawberry.mutation(
        permission_classes=[CanCreateStudentGuardian],
    )
    def create_student_guardian(
        self,
        input: CreateStudentGuardianInput,
    ) -> StudentGuardianType:
        return create_student_guardian_service(
            student_id=input.student_id,
            guardian_id=input.guardian_id,
            relationship=input.relationship.value,
            is_primary=input.is_primary,
        )

    @strawberry.mutation(
        permission_classes=[CanUpdateStudentGuardian],
    )
    def update_student_guardian(
        self,
        input: UpdateStudentGuardianInput,
    ) -> StudentGuardianType:
        return update_student_guardian_service(
            student_guardian_id=input.student_guardian_id,
            relationship=input.relationship.value,
            is_primary=input.is_primary,
        )

    @strawberry.mutation(
        permission_classes=[CanActivateStudentGuardian],
    )
    def activate_student_guardian(
        self,
        input: ActivateStudentGuardianInput,
    ) -> StudentGuardianType:
        return activate_student_guardian_service(
            student_guardian_id=input.student_guardian_id,
        )

    @strawberry.mutation(
        permission_classes=[CanDeactivateStudentGuardian],
    )
    def deactivate_student_guardian(
        self,
        input: DeactivateStudentGuardianInput,
    ) -> StudentGuardianType:
        return deactivate_student_guardian_service(
            student_guardian_id=input.student_guardian_id,
        )