from django.contrib import admin

from schools.models import AcademicTerm

@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "session",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter =(
        "session",
        "is_current",
    )

    search_fields = (
        "name",
        "session__name",
    )

    ordering = (
        "start_date",
    )
