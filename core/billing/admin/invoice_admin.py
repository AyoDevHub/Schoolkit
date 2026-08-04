from django.contrib import admin

from billing.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "student",
        "academic_session",
        "academic_term",
        "status",
        "total_amount",
        "due_date",
    )

    list_filter = (
        "status",
        "academic_session",
        "academic_term",
        "due_date",
    )

    search_fields = (
        "invoice_number",
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
        "fee_schedule",
    )

    readonly_fields = (
        "id",
        "invoice_number",
        "subtotal",
        "discount_total",
        "total_amount",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Invoice Information",
            {
                "fields": (
                    "school",
                    "student",
                    "academic_session",
                    "academic_term",
                    "fee_schedule",
                    "invoice_number",
                    "status",
                    "due_date",
                    "notes",
                ),
            },
        ),
        (
            "Financial Summary",
            {
                "fields": (
                    "subtotal",
                    "discount_total",
                    "total_amount",
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