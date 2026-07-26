import uuid

from django.db import models


class EnrollmentStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    PROMOTED = "promoted", "Promoted"
    TRANSFERRED = "transferred", "Transferred"
    WITHDRAWN = "withdrawn", "Withdrawn"
    GRADUATED = "graduated", "Graduated"


class Enrollment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    academic_session = models.ForeignKey(
        "schools.AcademicSession",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    academic_term = models.ForeignKey(
        "schools.AcademicTerm",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    class_level = models.ForeignKey(
        "schools.ClassLevel",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    class_arm = models.ForeignKey(
        "schools.ClassArm",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.ACTIVE,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "people_enrollments"
        ordering = [
            "-academic_session__start_date",
            "student__last_name",
            "student__first_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_session",
                ],
                name="unique_student_enrollment_per_session",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.student.full_name} - "
            f"{self.class_level.name} "
            f"{self.class_arm.name} "
            f"({self.academic_session.name})"
        )