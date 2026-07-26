from django.contrib import admin

from people.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "admission_number",
        "first_name",
        "last_name",
        "school",
        "is_active",
    )

    list_filter = (
        "school",
        "gender",
        "is_active",
    )

    search_fields = (
        "admission_number",
        "first_name",
        "last_name",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Student Information",
            {
                "fields": (
                    "school",
                    "admission_number",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "gender",
                    "date_of_birth",
                    "admission_date",
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