from django.contrib import admin

from billing.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "invoice",
        "amount",
        "payment_method",
        "status",
        "reference",
        "payment_date",
    )

    list_filter = (
        "payment_method",
        "status",
        "payment_date",
    )

    search_fields = (
        "invoice__invoice_number",
        "reference",
        "invoice__student__admission_number",
        "invoice__student__first_name",
        "invoice__student__last_name",
    )

    autocomplete_fields = (
        "invoice",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "invoice",
                    "amount",
                    "payment_method",
                    "status",
                    "reference",
                    "payment_date",
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