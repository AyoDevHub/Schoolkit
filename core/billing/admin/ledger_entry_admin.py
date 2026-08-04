from django.contrib import admin

from billing.models import LedgerEntry


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "transaction_type",
        "entry_type",
        "amount",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "entry_type",
        "created_at",
    )

    search_fields = (
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "student__middle_name",
        "notes",
    )

    autocomplete_fields = (
        "student",
        "invoice",
        "payment",
        "discount",
        "student_credit",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Ledger Information",
            {
                "fields": (
                    "student",
                    "transaction_type",
                    "entry_type",
                    "amount",
                    "invoice",
                    "payment",
                    "discount",
                    "student_credit",
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