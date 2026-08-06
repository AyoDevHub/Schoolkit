import strawberry
import strawberry_django

from billing.models import WebhookEvent


@strawberry_django.type(WebhookEvent)
class WebhookEventType:
    id: strawberry.auto
    provider: strawberry.auto
    event_id: strawberry.auto
    event_type: strawberry.auto
    signature: strawberry.auto
    payload: strawberry.auto
    status: strawberry.auto
    processed_at: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto