import uuid

from django.db import models



class FeeSchedule(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.PROTECT,
        related_name="fee_schedules",
    )

    academic_session = models.ForeignKey(
        "schools.AcademicSession",
        on_delete=models.PROTECT,
        related_name="fee_schedules",
    )

    academic_term = models.ForeignKey(
        "schools.AcademicTerm",
        on_delete=models.PROTECT,
        related_name="fee_schedules",
    )

    class_level = models.ForeignKey(
        "schools.ClassLevel",
        on_delete=models.PROTECT,
        related_name="fee_schedules",
    )

    is_active = models.BooleanField(
        default=True,
    )

    due_date = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_fee_schedules"

        ordering = [
            "class_level",
            "academic_session",
            "academic_term",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "school",
                    "academic_session",
                    "academic_term",
                    "class_level",
                ],
                name="unique_fee_schedule_per_class_session_term",
            ),
        ]

    def __str__(self):
        return (
            f"{self.class_level} - "
            f"{self.academic_term} "
            f"({self.academic_session})"
        )
