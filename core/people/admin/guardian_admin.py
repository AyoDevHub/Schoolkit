from django.contrib import admin

from people.models import Guardian


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "phone_number",
        "email",
        "school",
        "receive_sms",
        "receive_email",
        "is_active",
    )

    list_filter = (
        "school",
        "receive_sms",
        "receive_email",
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "middle_name",
        "phone_number",
        "email",
    )

    ordering = (
        "last_name",
        "first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Guardian Information",
            {
                "fields": (
                    "school",
                    "title",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "phone_number",
                    "email",
                    "home_address",
                    "is_active",
                )
            },
        ),
        (
            "Notification Preferences",
            {
                "fields": (
                    "receive_sms",
                    "receive_email",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )