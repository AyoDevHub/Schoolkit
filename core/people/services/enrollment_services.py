from django.core.exceptions import ValidationError
from django.db import transaction

from people.models import Enrollment, Student, EnrollmentStatus
from schools.models import (
    AcademicSession,
    AcademicTerm,
    ClassArm,
    ClassLevel,
    School,
)


@transaction.atomic
def create_enrollment(
    *,
    school_id: str,
    student_id: str,
    academic_session_id: str,
    academic_term_id: str,
    class_level_id: str,
    class_arm_id: str,
) -> Enrollment:

    # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })

    # Validate student exists
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id": "Student with the provided ID does not exist."
        })

    # Validate academic session exists
    try:
        academic_session = AcademicSession.objects.get(
            id=academic_session_id,
        )
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "academic_session_id": (
                "Academic session with the provided ID does not exist."
            )
        })

    # Validate academic term exists
    try:
        academic_term = AcademicTerm.objects.get(
            id=academic_term_id,
        )
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "academic_term_id": (
                "Academic term with the provided ID does not exist."
            )
        })

    # Validate class level exists
    try:
        class_level = ClassLevel.objects.get(
            id=class_level_id,
        )
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": (
                "Class level with the provided ID does not exist."
            )
        })

    # Validate class arm exists
    try:
        class_arm = ClassArm.objects.get(
            id=class_arm_id,
        )
    except ClassArm.DoesNotExist:
        raise ValidationError({
            "class_arm_id": (
                "Class arm with the provided ID does not exist."
            )
        })

    # Validate student belongs to school
    if student.school != school:
        raise ValidationError({
            "student_id": (
                "The selected student does not belong to this school."
            )
        })

    # Validate academic session belongs to school
    if academic_session.school != school:
        raise ValidationError({
            "academic_session_id": (
                "The selected academic session does not belong to this school."
            )
        })

    # Validate academic term belongs to school
    if academic_term.school != school:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to this school."
            )
        })

    # Validate class level belongs to school
    if class_level.school != school:
        raise ValidationError({
            "class_level_id": (
                "The selected class level does not belong to this school."
            )
        })

    # Validate class arm belongs to school
    if class_arm.school != school:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to this school."
            )
        })

    # Validate academic term belongs to academic session
    if academic_term.academic_session != academic_session:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to the selected academic session."
            )
        })

    # Validate class arm belongs to class level
    if class_arm.class_level != class_level:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to the selected class level."
            )
        })

    # Validate duplicate enrollment
    if Enrollment.objects.filter(
            student=student,
            academic_session=academic_session,
    ).exists():
        raise ValidationError({
            "student_id": (
                "The student is already enrolled for the selected academic session."
             )
        })

    # Validate academic term is active
    if not academic_term.is_active:
        raise ValidationError({
            "academic_term_id": (
                "Students can only be enrolled into the current active academic term."
            )
        })

    

    # Create enrollment
    enrollment = Enrollment(
        school=school,
        student=student,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
        class_arm=class_arm,
    )

    enrollment.save()

    return enrollment


@transaction.atomic
def update_enrollment(
    *,
    enrollment_id: str,
    academic_term_id: str | None = None,
    class_level_id: str | None = None,
    class_arm_id: str | None = None,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })

    # Build new values
    new_academic_term = enrollment.academic_term
    new_class_level = enrollment.class_level
    new_class_arm = enrollment.class_arm

    # Validate academic term
    if academic_term_id is not None:
        try:
            new_academic_term = AcademicTerm.objects.get(
                id=academic_term_id,
            )
        except AcademicTerm.DoesNotExist:
            raise ValidationError({
                "academic_term_id": (
                    "Academic term with the provided ID does not exist."
                )
            })

    # Validate class level
    if class_level_id is not None:
        try:
            new_class_level = ClassLevel.objects.get(
                id=class_level_id,
            )
        except ClassLevel.DoesNotExist:
            raise ValidationError({
                "class_level_id": (
                    "Class level with the provided ID does not exist."
                )
            })

    # Validate class arm
    if class_arm_id is not None:
        try:
            new_class_arm = ClassArm.objects.get(
                id=class_arm_id,
            )
        except ClassArm.DoesNotExist:
            raise ValidationError({
                "class_arm_id": (
                    "Class arm with the provided ID does not exist."
                )
            })

    # Validate academic term belongs to the enrollment's school
    if new_academic_term.school != enrollment.school:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to this school."
            )
        })

    # Validate class level belongs to the enrollment's school
    if new_class_level.school != enrollment.school:
        raise ValidationError({
            "class_level_id": (
                "The selected class level does not belong to this school."
            )
        })

    # Validate class arm belongs to the enrollment's school
    if new_class_arm.school != enrollment.school:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to this school."
            )
        })

    # Validate academic term belongs to the enrollment's academic session
    if new_academic_term.academic_session != enrollment.academic_session:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to the enrollment's academic session."
            )
        })

    # Validate class arm belongs to the selected class level
    if new_class_arm.class_level != new_class_level:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to the selected class level."
            )
        })

    # Assign values
    enrollment.academic_term = new_academic_term
    enrollment.class_level = new_class_level
    enrollment.class_arm = new_class_arm

    enrollment.save()

    return enrollment


@transaction.atomic
def activate_enrollment(
    *,
    enrollment_id: str,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })


    # Validate enrollment can be reactivated
    if enrollment.status in [
        EnrollmentStatus.PROMOTED,
        EnrollmentStatus.TRANSFERRED,
        EnrollmentStatus.WITHDRAWN,
    ]:
        raise ValidationError({
            "enrollment_id": (
                "Only manually deactivated enrollments can be reactivated."
            )
        })

    
    # Reactivate enrollment
    enrollment.is_active = True
    enrollment.status = EnrollmentStatus.ACTIVE

    enrollment.save()

    return enrollment


@transaction.atomic
def deactivate_enrollment(
    *,
    enrollment_id: str,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })

    # Already inactive
    if not enrollment.is_active:
        return enrollment

    # Deactivate enrollment
    enrollment.is_active = False

    enrollment.save()

    return enrollment


@transaction.atomic
def withdraw_student(
    *,
    enrollment_id: str,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })

   # Validate enrollment can be withdrawn
    if (
        not enrollment.is_active
        or enrollment.status != EnrollmentStatus.ACTIVE
    ):
        raise ValidationError({
            "enrollment_id": (
                "Only active enrollments can be be withdrawn."
            )
        })


    # Withdraw enrollment
    enrollment.status = EnrollmentStatus.WITHDRAWN
    enrollment.is_active = False

    enrollment.save()

    return enrollment


@transaction.atomic
def promote_student(
    *,
    enrollment_id: str,
    academic_session_id: str,
    academic_term_id: str,
    class_level_id: str,
    class_arm_id: str,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })

    # Validate enrollment can be promoted
    if (
        not enrollment.is_active
        or enrollment.status != EnrollmentStatus.ACTIVE
    ):
        raise ValidationError({
            "enrollment_id": (
                "Only active enrollments can be promoted."
            )
        })

    # Validate academic session exists
    try:
        academic_session = AcademicSession.objects.get(
            id=academic_session_id,
        )
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "academic_session_id": (
                "Academic session with the provided ID does not exist."
            )
        })

    # Validate academic term exists
    try:
        academic_term = AcademicTerm.objects.get(
            id=academic_term_id,
        )
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "academic_term_id": (
                "Academic term with the provided ID does not exist."
            )
        })

    # Validate class level exists
    try:
        class_level = ClassLevel.objects.get(
            id=class_level_id,
        )
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": (
                "Class level with the provided ID does not exist."
            )
        })

    # Validate class arm exists
    try:
        class_arm = ClassArm.objects.get(
            id=class_arm_id,
        )
    except ClassArm.DoesNotExist:
        raise ValidationError({
            "class_arm_id": (
                "Class arm with the provided ID does not exist."
            )
        })

    # Validate academic session belongs to the school
    if academic_session.school != enrollment.school:
        raise ValidationError({
            "academic_session_id": (
                "The selected academic session does not belong to this school."
            )
        })

    # Validate academic term belongs to the school
    if academic_term.school != enrollment.school:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to this school."
            )
        })

    # Validate class level belongs to the school
    if class_level.school != enrollment.school:
        raise ValidationError({
            "class_level_id": (
                "The selected class level does not belong to this school."
            )
        })

    # Validate class arm belongs to the school
    if class_arm.school != enrollment.school:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to this school."
            )
        })

    # Validate academic term belongs to the academic session
    if academic_term.academic_session != academic_session:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to the selected academic session."
            )
        })

    # Validate class arm belongs to the class level
    if class_arm.class_level != class_level:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to the selected class level."
            )
        })

    # Validate promotion is to a different academic session
    if academic_session == enrollment.academic_session:
        raise ValidationError({
            "academic_session_id": (
                "A student cannot be promoted into the same academic session."
            )
        })

    # Validate duplicate enrollment
    if Enrollment.objects.filter(
        student=enrollment.student,
        academic_session=academic_session,
    ).exists():
        raise ValidationError({
            "student_id": (
                "The student is already enrolled for the selected academic session."
            )
        })

    # Close current enrollment
    enrollment.status = EnrollmentStatus.PROMOTED
    enrollment.is_active = False
    enrollment.save()

        # Create new enrollment
    new_enrollment = Enrollment(
        school=enrollment.school,
        student=enrollment.student,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
        class_arm=class_arm,
    )

    new_enrollment.save()


    return new_enrollment


@transaction.atomic
def transfer_student(
    *,
    enrollment_id: str,
    academic_session_id: str,
    academic_term_id: str,
    class_level_id: str,
    class_arm_id: str,
) -> Enrollment:

    # Validate enrollment exists
    try:
        enrollment = Enrollment.objects.get(
            id=enrollment_id,
        )
    except Enrollment.DoesNotExist:
        raise ValidationError({
            "enrollment_id": (
                "Enrollment with the provided ID does not exist."
            )
        })

    # Validate enrollment can be transferred
    if (
        not enrollment.is_active
        or enrollment.status != EnrollmentStatus.ACTIVE
    ):
        raise ValidationError({
            "enrollment_id": (
                "Only active enrollments can be transferred."
            )
        })

    # Validate academic session exists
    try:
        academic_session = AcademicSession.objects.get(
            id=academic_session_id,
        )
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "academic_session_id": (
                "Academic session with the provided ID does not exist."
            )
        })

    # Validate academic term exists
    try:
        academic_term = AcademicTerm.objects.get(
            id=academic_term_id,
        )
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "academic_term_id": (
                "Academic term with the provided ID does not exist."
            )
        })

    # Validate class level exists
    try:
        class_level = ClassLevel.objects.get(
            id=class_level_id,
        )
    except ClassLevel.DoesNotExist:
        raise ValidationError({
            "class_level_id": (
                "Class level with the provided ID does not exist."
            )
        })

    # Validate class arm exists
    try:
        class_arm = ClassArm.objects.get(
            id=class_arm_id,
        )
    except ClassArm.DoesNotExist:
        raise ValidationError({
            "class_arm_id": (
                "Class arm with the provided ID does not exist."
            )
        })

    # Validate academic session belongs to the school
    if academic_session.school != enrollment.school:
        raise ValidationError({
            "academic_session_id": (
                "The selected academic session does not belong to this school."
            )
        })

    # Validate academic term belongs to the school
    if academic_term.school != enrollment.school:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to this school."
            )
        })

    # Validate class level belongs to the school
    if class_level.school != enrollment.school:
        raise ValidationError({
            "class_level_id": (
                "The selected class level does not belong to this school."
            )
        })

    # Validate class arm belongs to the school
    if class_arm.school != enrollment.school:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to this school."
            )
        })

    # Validate academic term belongs to the academic session
    if academic_term.academic_session != academic_session:
        raise ValidationError({
            "academic_term_id": (
                "The selected academic term does not belong to the selected academic session."
            )
        })

    # Validate class arm belongs to the class level
    if class_arm.class_level != class_level:
        raise ValidationError({
            "class_arm_id": (
                "The selected class arm does not belong to the selected class level."
            )
        })

    # Validate duplicate enrollment
    if Enrollment.objects.filter(
    student=enrollment.student,
    academic_session=academic_session,
    class_level=class_level,
    class_arm=class_arm,
    is_active=True,
    ).exists():
     raise ValidationError({
         "enrollment_id": (
             "The student is already enrolled in the selected academic session, class level, and class arm."
         )
     })
    
    # Close current enrollment
    enrollment.status = EnrollmentStatus.TRANSFERRED
    enrollment.is_active = False
    enrollment.save()

    # Create new enrollment
    new_enrollment = Enrollment(
        school=enrollment.school,
        student=enrollment.student,
        academic_session=academic_session,
        academic_term=academic_term,
        class_level=class_level,
        class_arm=class_arm,
    )

    new_enrollment.save()

    return new_enrollment