from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from billing.models import (
    WebhookEvent,
    WebhookEventStatus,
)


@transaction.atomic
def create_webhook_event(
    *,
    provider: str,
    event_id: str,
    event_type: str,
    signature: str,
    payload: dict,
) -> WebhookEvent:

    # Prevent duplicate webhook events
    if WebhookEvent.objects.filter(
        provider=provider,
        event_id=event_id,
    ).exists():
        raise ValidationError({
            "event_id": (
                "This webhook event has "
                "already been received."
            )
        })

    webhook_event = WebhookEvent.objects.create(
        provider=provider,
        event_id=event_id,
        event_type=event_type,
        signature=signature,
        payload=payload,
        status=WebhookEventStatus.PENDING,
    )

    return webhook_event


@transaction.atomic
def mark_webhook_processed(
    *,
    webhook_event: WebhookEvent,
) -> WebhookEvent:

    if webhook_event.status == WebhookEventStatus.PROCESSED:
        return webhook_event

    webhook_event.status = WebhookEventStatus.PROCESSED
    webhook_event.processed_at = timezone.now()

    webhook_event.save(
        update_fields=[
            "status",
            "processed_at",
            "updated_at",
        ],
    )

    return webhook_event


@transaction.atomic
def mark_webhook_failed(
    *,
    webhook_event: WebhookEvent,
) -> WebhookEvent:

    if webhook_event.status == WebhookEventStatus.FAILED:
        return webhook_event

    webhook_event.status = WebhookEventStatus.FAILED

    webhook_event.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return webhook_event