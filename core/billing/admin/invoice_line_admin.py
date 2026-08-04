from django.contrib import admin

from billing.models import InvoiceLine


@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):

    list_display = (
        "invoice",
        "fee_item",
        "amount",
    )

    list_filter = (
        "fee_item",
    )

    search_fields = (
        "invoice__invoice_number",
        "fee_item__name",
        "invoice__student__admission_number",
        "invoice__student__first_name",
        "invoice__student__last_name",
    )

    autocomplete_fields = (
        "invoice",
        "fee_item",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Invoice Line Information",
            {
                "fields": (
                    "invoice",
                    "fee_item",
                    "amount",
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