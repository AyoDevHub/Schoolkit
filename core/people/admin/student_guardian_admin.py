from django.contrib import admin

from people.models import StudentGuardian


@admin.register(StudentGuardian)
class StudentGuardianAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "guardian",
        "relationship",
        "is_primary",
        "is_active",
    )

    list_filter = (
        "relationship",
        "is_primary",
        "is_active",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "guardian__first_name",
        "guardian__last_name",
        "guardian__phone_number",
    )

    ordering = (
        "student__last_name",
        "student__first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Relationship Information",
            {
                "fields": (
                    "student",
                    "guardian",
                    "relationship",
                    "is_primary",
                    "is_active",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )