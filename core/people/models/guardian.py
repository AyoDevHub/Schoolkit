import uuid

from django.db import models


class Title(models.TextChoices):
    MR = "mr", "Mr."
    MRS = "mrs", "Mrs."
    MISS = "miss", "Miss"
    MS = "ms", "Ms."


class Guardian(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="guardians",
    )

    title = models.CharField(
        max_length=20,
        choices=Title.choices,
        blank=True,
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

    phone_number = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        blank=True,
    )

    home_address = models.TextField(
        blank=True,
    )

    receive_sms = models.BooleanField(
        default=True,
    )

    receive_email = models.BooleanField(
        default=True,
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
        db_table = "people_guardians"
        ordering = [
            "last_name",
            "first_name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "phone_number"],
                name="unique_guardian_phone_per_school",
            )
        ]

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return " ".join(
            filter(
                None,
                [
                    self.get_title_display() if self.title else "",
                    self.first_name,
                    self.middle_name,
                    self.last_name,
                ],
            )
        )