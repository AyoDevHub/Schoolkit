import uuid

from django.db import models 


class TermName(models.TextChoices):
    FIRST = "FIRST", "First Term"
    SECOND = "SECOND", "Second Term"
    THIRD = "THIRD", "Third Term"


class AcademicTerm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, 
        editable=False,
    )
    
    session = models.ForeignKey(
        "schools.AcademicSession",
        on_delete=models.CASCADE,
        related_name="academic_terms",
    )
    
    name = models.CharField(
        max_length=20,
        choices=TermName.choices,
    )

    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        db_table = "schools_academic_terms"
        ordering = ["start_date",]
        constraints = [
            models.UniqueConstraint(
                fields=["session", "name"],
                name="unique_term_per_session",
            )
        ]


    def __str__(self):
        return f"{self.session.school.name} - {self.session.name} - {self.name}"