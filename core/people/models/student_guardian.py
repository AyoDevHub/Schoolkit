import uuid

from django.db import models


class RelationshipType(models.TextChoices):
    FATHER = "father", "Father"
    MOTHER = "mother", "Mother"
    GUARDIAN = "guardian", "Guardian"
    UNCLE = "uncle", "Uncle"
    AUNT = "aunt", "Aunt"
    GRANDFATHER = "grandfather", "Grandfather"
    GRANDMOTHER = "grandmother", "Grandmother"
    BROTHER = "brother", "Brother"
    SISTER = "sister", "Sister"


class StudentGuardian(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.CASCADE,
        related_name="guardian_links",
    )

    guardian = models.ForeignKey(
        "people.Guardian",
        on_delete=models.CASCADE,
        related_name="student_links",
    )

    relationship = models.CharField(
        max_length=20,
        choices=RelationshipType.choices,
    )

    is_primary = models.BooleanField(
        default=False,
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
        db_table = "people_student_guardians"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "guardian"],
                name="unique_student_guardian",
            ),
        ]

    def __str__(self):
        return (
            f"{self.student.full_name} "
            f"({self.get_relationship_display()}: "
            f"{self.guardian.full_name})"
        )