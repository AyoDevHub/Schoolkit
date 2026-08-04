from django.contrib import admin

from billing.models import FeeSchedule


@admin.register(FeeSchedule)
class FeeScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "class_level",
        "academic_session",
        "academic_term",
        "school",
        "is_active",
        "due_date",
    )

    list_filter = (
        "school",
        "academic_session",
        "academic_term",
        "class_level",
        "is_active",
    )

    search_fields = (
        "class_level__name",
        "academic_session__name",
        "academic_term__name",
    )

    ordering = (
        "class_level",
        "academic_session",
        "academic_term",
    )

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    def has_delete_permission(self, request, obj=None):
        return False