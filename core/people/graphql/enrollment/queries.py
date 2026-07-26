import strawberry

from people.graphql.enrollment.types import EnrollmentType
from people.graphql.permissions import (
    CanViewEnrollments,
)
from people.selectors.enrollment_selectors import (
    get_enrollment_by_id,
    list_active_enrollments,
    list_enrollments,
    list_enrollments_by_academic_session,
    list_enrollments_by_academic_term,
    list_enrollments_by_class,
    list_enrollments_by_school,
    list_enrollments_by_student,
    list_inactive_enrollments,
)


@strawberry.type
class EnrollmentQuery:

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollment(
        self,
        enrollment_id: str,
    ) -> EnrollmentType | None:
        return get_enrollment_by_id(
            enrollment_id=enrollment_id,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def active_enrollments(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_active_enrollments(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def inactive_enrollments(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_inactive_enrollments(
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments_by_school(
        self,
        school_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments_by_school(
            school_id=school_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments_by_student(
        self,
        student_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments_by_student(
            student_id=student_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments_by_academic_session(
        self,
        academic_session_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments_by_academic_session(
            academic_session_id=academic_session_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments_by_academic_term(
        self,
        academic_term_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments_by_academic_term(
            academic_term_id=academic_term_id,
            offset=offset,
            limit=limit,
        )

    @strawberry.field(
        permission_classes=[CanViewEnrollments],
    )
    def enrollments_by_class(
        self,
        class_level_id: str,
        class_arm_id: str,
        offset: int = 0,
        limit: int = 10,
    ) -> list[EnrollmentType]:
        return list_enrollments_by_class(
            class_level_id=class_level_id,
            class_arm_id=class_arm_id,
            offset=offset,
            limit=limit,
        )