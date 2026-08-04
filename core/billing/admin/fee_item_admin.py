from django.contrib import admin

from billing.models import FeeItem


@admin.register(FeeItem)
class FeeItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "school",
        "is_active",
        "created_at",
        "is_recurring",
    ]

    search_fields = [
        "name",
        "school__name",
    ]

    list_filter = [
        "school",
        "is_active",
    ]

    list_select_related = [
        "school",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    def has_delete_permission(self, request, obj=None):
        return False