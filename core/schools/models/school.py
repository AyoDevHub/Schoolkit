import uuid

from django.db import models


class School(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    code = models.CharField(
        max_length=20,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="schools/logos/",
        blank=True,
        null=True,
    )

    website = models.URLField(
        blank=True,
    )

    motto = models.CharField(
        max_length=255,
        blank=True,
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
        db_table = "schools_school"
        ordering = ["name"]

    def __str__(self):
        return self.name