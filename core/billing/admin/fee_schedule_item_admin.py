from django.contrib import admin

from billing.models import FeeScheduleItem


@admin.register(FeeScheduleItem)
class FeeScheduleItemAdmin(admin.ModelAdmin):

    list_display = (
        "fee_schedule",
        "fee_item",
        "amount",
        "created_at",
    )

    list_filter = (
        "fee_schedule__school",
        "fee_schedule__academic_session",
        "fee_schedule__academic_term",
        "fee_schedule__class_level",
        "fee_item",
    )

    search_fields = (
        "fee_item__name",
        "fee_schedule__class_level__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "fee_schedule",
        "fee_item",
    )

    def has_delete_permission(self, request, obj=None):
        return False