import strawberry

from people.graphql.enrollment.inputs import (
    ActivateEnrollmentInput,
    CreateEnrollmentInput,
    DeactivateEnrollmentInput,
    PromoteStudentInput,
    TransferStudentInput,
    UpdateEnrollmentInput,
    WithdrawStudentInput,
)
from people.graphql.enrollment.types import EnrollmentType
from people.graphql.permissions import (
    CanActivateEnrollment,
    CanCreateEnrollment,
    CanDeactivateEnrollment,
    CanPromoteStudent,
    CanTransferStudent,
    CanUpdateEnrollment,
    CanWithdrawStudent,
)
from people.services.enrollment_services import (
    activate_enrollment,
    create_enrollment,
    deactivate_enrollment,
    promote_student,
    transfer_student,
    update_enrollment,
    withdraw_student,
)


@strawberry.type
class EnrollmentMutation:

    @strawberry.mutation(
        permission_classes=[CanCreateEnrollment],
    )
    def create_enrollment(
        self,
        input: CreateEnrollmentInput,
    ) -> EnrollmentType:
        return create_enrollment(
        school_id=input.school_id,
        student_id=input.student_id,
        academic_session_id=input.academic_session_id,
        academic_term_id=input.academic_term_id,
        class_level_id=input.class_level_id,
        class_arm_id=input.class_arm_id,
    )

    @strawberry.mutation(
        permission_classes=[CanUpdateEnrollment],
    )
    def update_enrollment(
        self,
        input: UpdateEnrollmentInput,
    ) -> EnrollmentType:
        return update_enrollment(
        enrollment_id=input.enrollment_id,
        academic_term_id=input.academic_term_id,
        class_level_id=input.class_level_id,
        class_arm_id=input.class_arm_id,
    )

    @strawberry.mutation(
        permission_classes=[CanActivateEnrollment],
    )
    def activate_enrollment(
        self,
        input: ActivateEnrollmentInput,
    ) -> EnrollmentType:
        return activate_enrollment(
            enrollment_id=input.enrollment_id,
        )

    @strawberry.mutation(
        permission_classes=[CanDeactivateEnrollment],
    )
    def deactivate_enrollment(
        self,
        input: DeactivateEnrollmentInput,
    ) -> EnrollmentType:
        return activate_enrollment(
            enrollment_id=input.enrollment_id,
        )

    @strawberry.mutation(
        permission_classes=[CanWithdrawStudent],
    )
    def withdraw_student(
        self,
        input: WithdrawStudentInput,
    ) -> EnrollmentType:
        return activate_enrollment(
            enrollment_id=input.enrollment_id,
        )

    @strawberry.mutation(
        permission_classes=[CanPromoteStudent],
    )
    def promote_student(
        self,
        input: PromoteStudentInput,
    ) -> EnrollmentType:
        return promote_student(
            enrollment_id=input.enrollment_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            class_level_id=input.class_level_id,
            class_arm_id=input.class_arm_id,
        )

    @strawberry.mutation(
        permission_classes=[CanTransferStudent],
    )
    def transfer_student(
        self,
        input: TransferStudentInput,
    ) -> EnrollmentType:
        return transfer_student(
            enrollment_id=input.enrollment_id,
            academic_session_id=input.academic_session_id,
            academic_term_id=input.academic_term_id,
            class_level_id=input.class_level_id,
            class_arm_id=input.class_arm_id,
        )