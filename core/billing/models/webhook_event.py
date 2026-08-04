import uuid

from django.db import models


class WebhookEventStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSED = "processed", "Processed"
    FAILED = "failed", "Failed"


class WebhookEvent(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    event_id = models.CharField(
        max_length=100,
    )

    event_type = models.CharField(
        max_length=100,
    )

    signature = models.CharField(
        max_length=255,
    )

    payload = models.JSONField()

    provider = models.CharField(
        max_length=50,
        default="paystack",
    )

    status = models.CharField(
        max_length=20,
        choices=WebhookEventStatus.choices,
        default=WebhookEventStatus.PENDING,
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "billing_webhook_events"

        ordering = [
            "-created_at",
        ]

        constraints = [
        models.UniqueConstraint(
            fields=[
                "provider",
                "event_id",
            ],
            name="unique_provider_event_id",
        ),
        ]

    def __str__(self):
        return self.event_id