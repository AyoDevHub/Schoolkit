import uuid

from django.db import models


class DiscountCategory(models.TextChoices):
        DISCOUNT = "DISCOUNT", "Discount"
        SCHOLARSHIP = "SCHOLARSHIP", "Scholarship"
        WAIVER = "WAIVER", "Waiver"


class ValueType(models.TextChoices):
    PERCENTAGE = "PERCENTAGE", "Percentage"
    FIXED_AMOUNT = "FIXED_AMOUNT", "Fixed Amount"


class Discount(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    school = models.ForeignKey(
        "schools.School",
        on_delete=models.PROTECT,
        related_name="discounts",
    )

    student = models.ForeignKey(
        "people.Student",
        on_delete=models.PROTECT,
        related_name="discounts",
    )

    academic_session = models.ForeignKey(
        "schools.AcademicSession",
        on_delete=models.PROTECT,
        related_name="discounts",
    )

    academic_term = models.ForeignKey(
        "schools.AcademicTerm",
        on_delete=models.PROTECT,
        related_name="discounts",
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DiscountCategory.choices,
    )

    value_type = models.CharField(
        max_length=20,
        choices=ValueType.choices,
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reason = models.TextField(
        blank=True,
    )

    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="approved_discounts",
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
        db_table = "billing_discounts"

        ordering = [
            "student",
            "academic_session",
            "academic_term",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "school",
                    "student",
                    "academic_session",
                    "academic_term",
                    "discount_type",
                ],
                name="unique_discount_per_student_term_type",
            ),
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.discount_type}"
        )