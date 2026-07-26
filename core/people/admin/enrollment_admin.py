from django.contrib import admin

from people.models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "academic_session",
        "academic_term",
        "class_level",
        "class_arm",
        "status",
        "is_active",
    )

    list_filter = (
        "academic_session",
        "academic_term",
        "class_level",
        "class_arm",
        "status",
        "is_active",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
    )

    autocomplete_fields = (
        "student",
        "academic_session",
        "academic_term",
        "class_level",
        "class_arm",
    )

    ordering = (
        "-academic_session__start_date",
        "student__last_name",
    )