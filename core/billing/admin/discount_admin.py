from django.contrib import admin

from billing.models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "discount_type",
        "value_type",
        "value",
        "academic_session",
        "academic_term",
        "approved_by",
        "is_active",
    )

    list_filter = (
        "discount_type",
        "value_type",
        "academic_session",
        "academic_term",
        "is_active",
    )
    
    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "student__middle_name",
        "school__name",
    )

    autocomplete_fields = (
        "school",
        "student",
        "academic_session",
        "academic_term",
        "approved_by",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Discount Information",
            {
                "fields": (
                    "school",
                    "student",
                    "academic_session",
                    "academic_term",
                    "discount_type",
                    "value_type",
                    "value",
                    "reason",
                    "approved_by",
                    "is_active",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def has_delete_permission(
        self,
        request,
        obj=None,
    ):
        return False