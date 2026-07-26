import uuid

from django.db import models


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="students",
    )


    admission_number = models.CharField(
        max_length=50,
        db_index=True
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    date_of_birth = models.DateField()

    admission_date = models.DateField()

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
        db_table = "people_students"
        ordering = [
            "last_name",
            "first_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "admission_number"],
                name="unique_student_admission_number_per_school",
            )
        ]

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"
    

    @property
    def full_name(self) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.first_name,
                    self.middle_name,
                    self.last_name,
                ],
            )
        )
