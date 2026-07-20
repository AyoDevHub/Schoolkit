import uuid

from django.db import models


class Subject(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="subjects",
    )

    name = models.CharField(
        max_length=100,
    )

    levels = models.ManyToManyField(
        "schools.ClassLevel",
        related_name="subjects",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "subjects"
        ordering = [
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "name"],
                name="unique_subject_per_school",
            )
        ]

    def __str__(self):
        return f"{self.school.name} - {self.name}"