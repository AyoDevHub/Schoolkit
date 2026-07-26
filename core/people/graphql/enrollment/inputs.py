import strawberry


@strawberry.input
class CreateEnrollmentInput:
    school_id: str
    student_id: str
    academic_session_id: str
    academic_term_id: str
    class_level_id: str
    class_arm_id: str


@strawberry.input
class UpdateEnrollmentInput:
    enrollment_id: str
    academic_term_id: str | None = None
    class_level_id: str | None = None
    class_arm_id: str | None = None


@strawberry.input
class ActivateEnrollmentInput:
    enrollment_id: str


@strawberry.input
class DeactivateEnrollmentInput:
    enrollment_id: str


@strawberry.input
class WithdrawStudentInput:
    enrollment_id: str


@strawberry.input
class PromoteStudentInput:
    enrollment_id: str
    academic_session_id: str
    academic_term_id: str
    class_level_id: str
    class_arm_id: str


@strawberry.input
class TransferStudentInput:
    enrollment_id: str
    academic_session_id: str
    academic_term_id: str
    class_level_id: str
    class_arm_id: str