import strawberry

from billing.graphql.webhook_event.types import (
    WebhookEventType,
)
from billing.selectors.webhook_event_selectors import (
    get_webhook_event_by_event_id,
    get_webhook_event_by_id,
    list_failed_webhook_events,
    list_pending_webhook_events,
    list_processed_webhook_events,
    list_webhook_events,
)


@strawberry.type
class WebhookEventQuery:

    @strawberry.field
    def webhook_event(
        self,
        id: strawberry.ID,
    ) -> WebhookEventType | None:
        return get_webhook_event_by_id(
            id=id,
        )

    @strawberry.field
    def webhook_event_by_event_id(
        self,
        event_id: str,
    ) -> WebhookEventType | None:
        return get_webhook_event_by_event_id(
            event_id=event_id,
        )

    @strawberry.field
    def webhook_events(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> list[WebhookEventType]:
        return list_webhook_events(
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def pending_webhook_events(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> list[WebhookEventType]:
        return list_pending_webhook_events(
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def processed_webhook_events(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> list[WebhookEventType]:
        return list_processed_webhook_events(
            offset=offset,
            limit=limit,
        )

    @strawberry.field
    def failed_webhook_events(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> list[WebhookEventType]:
        return list_failed_webhook_events(
            offset=offset,
            limit=limit,
        )