import uuid

from django.db import models


class ClassLevel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="class_levels",
    )

    name = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "schools_class_levels"
        ordering = [
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "name"],
                name="unique_class_level_per_school",
            ),
        ]

    def __str__(self):
        return f"{self.school.name} - {self.name}"
    



class ClassArm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    level = models.ForeignKey(
        "schools.ClassLevel",
        on_delete=models.CASCADE,
        related_name="class_arms",
    )

    name = models.CharField(
        max_length=10,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "schools_class_arms"
        ordering = [
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["level", "name"],
                name="unique_class_arm_per_level",
            ),
        ]

    def __str__(self):
        return f"{self.level.name} {self.name}"