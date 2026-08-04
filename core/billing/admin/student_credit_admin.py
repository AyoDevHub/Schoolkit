from django.contrib import admin

from billing.models import StudentCredit


@admin.register(StudentCredit)
class StudentCreditAdmin(admin.ModelAdmin):

    list_display = (
        "credit_note_number",
        "student",
        "reason",
        "amount",
        "remaining_amount",
        "is_active",
        "created_at",
    )

    list_filter = (
        "reason",
        "is_active",
        "created_at",
    )

    search_fields = (
        "credit_note_number",
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
    )

    readonly_fields = (
        "id",
        "credit_note_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Credit Information",
            {
                "fields": (
                    "student",
                    "invoice",
                    "payment",
                    "credit_note_number",
                    "reason",
                    "amount",
                    "remaining_amount",
                    "notes",
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