from django.contrib import admin

from schools.models import AcademicSession


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "school",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "school",
        "is_current",
    )

    search_fields = (
        "name",
        "school__name",
    )

    ordering = (
        "-start_date",
    )