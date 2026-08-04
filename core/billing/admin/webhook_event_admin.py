from django.contrib import admin

from billing.models import WebhookEvent


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):

    list_display = (
        "event_id",
        "provider",
        "event_type",
        "status",
        "processed_at",
        "created_at",
    )

    list_filter = (
        "provider",
        "status",
        "event_type",
    )

    search_fields = (
        "event_id",
        "event_type",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "processed_at",
        "payload",
        "signature",
    )