from django.contrib import admin

from billing.models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_number",
        "payment",
        "created_at",
    )

    search_fields = (
        "receipt_number",
        "payment__payment_reference",
        "payment__invoice__invoice_number",
        "payment__invoice__student__admission_number",
        "payment__invoice__student__first_name",
        "payment__invoice__student__last_name",
        "payment__invoice__student__middle_name",
        "notes",
    )

    autocomplete_fields = (
        "payment",
    )

    readonly_fields = (
        "id",
        "receipt_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Receipt Information",
            {
                "fields": (
                    "payment",
                    "receipt_number",
                    "notes",
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