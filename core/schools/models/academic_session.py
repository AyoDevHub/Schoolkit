from django.db import models
import uuid


class AcademicSession(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="academic_sessions",
    )

    name = models.CharField(
        max_length=20,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_current = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "schools_academic_sessions"

        ordering = [
            "-start_date",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["school", "name"],
                name="unique_session_per_school",
            )
        ]

    def __str__(self):
        return f"{self.school.name} - {self.name}"