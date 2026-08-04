from billing.models import WebhookEvent


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)
    return offset, limit


def get_webhook_event_by_id(
    *,
    id: str,
) -> WebhookEvent | None:
    return WebhookEvent.objects.filter(
        id=id,
    ).first()


def get_webhook_event_by_event_id(
    *,
    event_id: str,
) -> WebhookEvent | None:
    return WebhookEvent.objects.filter(
        event_id=event_id,
    ).first()


def list_webhook_events(
    *,
    offset: int = 0,
    limit: int = 50,
):

    offset, limit = _paginate(offset, limit)

    return WebhookEvent.objects.all()[
        offset: offset + limit
    ]


def list_pending_webhook_events(
    *,
    offset: int = 0,
    limit: int = 50,
):

    offset, limit = _paginate(offset, limit)

    return WebhookEvent.objects.filter(
        status="pending",
    )[
        offset: offset + limit
    ]


def list_processed_webhook_events(
    *,
    offset: int = 0,
    limit: int = 50,
):
    offset, limit = _paginate(offset, limit)

    return WebhookEvent.objects.filter(
        status="processed",
    )[
        offset: offset + limit
    ]


def list_failed_webhook_events(
    *,
    offset: int = 0,
    limit: int = 50,
):

    offset, limit = _paginate(offset, limit)
    
    return WebhookEvent.objects.filter(
        status="failed",
    )[
        offset: offset + limit
    ]