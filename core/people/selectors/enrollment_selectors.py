from people.models import Enrollment


def get_enrollment_by_id(
    *,
    enrollment_id: str,
) -> Enrollment | None:
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            id=enrollment_id,
        )
        .first()
    )


def list_enrollments(
    *,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .all()[
            offset : offset + limit
        ]
    )


def list_active_enrollments(
    *,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            is_active=True,
        )[
            offset : offset + limit
        ]
    )


def list_inactive_enrollments(
    *,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            is_active=False,
        )[
            offset : offset + limit
        ]
    )


def list_enrollments_by_school(
    *,
    school_id: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            school_id=school_id,
        )[
            offset : offset + limit
        ]
    )


def list_enrollments_by_student(
    *,
    student_id: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            student_id=student_id,
        )[
            offset : offset + limit
        ]
    )


def list_enrollments_by_academic_session(
    *,
    academic_session_id: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            academic_session_id=academic_session_id,
        )[
            offset : offset + limit
        ]
    )


def list_enrollments_by_academic_term(
    *,
    academic_term_id: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            academic_term_id=academic_term_id,
        )[
            offset : offset + limit
        ]
    )


def list_enrollments_by_class(
    *,
    class_level_id: str,
    class_arm_id: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        Enrollment.objects.select_related(
            "student",
            "school",
            "academic_session",
            "academic_term",
            "class_level",
            "class_arm",
        )
        .filter(
            class_level_id=class_level_id,
            class_arm_id=class_arm_id,
        )[
            offset : offset + limit
        ]
    )