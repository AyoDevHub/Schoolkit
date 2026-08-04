from billing.models import Receipt


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_receipt_by_id(
    receipt_id: str,
) -> Receipt:
    return Receipt.objects.get(
        id=receipt_id,
    )


def get_receipt_by_number(
    receipt_number: str,
) -> Receipt:
    return Receipt.objects.get(
        receipt_number=receipt_number,
    )


def get_receipt_by_payment(
    payment_id: str,
) -> Receipt:
    return Receipt.objects.get(
        payment_id=payment_id,
    )


def list_receipts(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Receipt.objects.filter(
        payment__invoice__student__school_id=school_id,
    )[offset:offset + limit]


def list_receipts_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Receipt.objects.filter(
        payment__invoice__student_id=student_id,
    )[offset:offset + limit]