from billing.models import InvoiceLine


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_invoice_line_by_id(
    invoice_line_id: str,
) -> InvoiceLine:
    return InvoiceLine.objects.get(
        id=invoice_line_id,
    )


def list_invoice_lines(
    invoice_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return InvoiceLine.objects.filter(
        invoice_id=invoice_id,
    )[offset:offset + limit]


def list_invoice_lines_by_fee_item(
    fee_item_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return InvoiceLine.objects.filter(
        fee_item_id=fee_item_id,
    )[offset:offset + limit]