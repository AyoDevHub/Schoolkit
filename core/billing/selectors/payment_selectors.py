from billing.models import Payment


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_payment_by_id(
    payment_id: str,
) -> Payment:
    return Payment.objects.get(
        id=payment_id,
    )


def get_payment_by_reference(
    reference: str,
) -> Payment:
    return Payment.objects.get(
        reference=reference,
    )


def list_payments(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Payment.objects.filter(
        invoice__school_id=school_id,
    )[offset:offset + limit]


def list_payments_by_invoice(
    invoice_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Payment.objects.filter(
        invoice_id=invoice_id,
    )[offset:offset + limit]


def list_payments_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Payment.objects.filter(
        invoice__student_id=student_id,
    )[offset:offset + limit]


def list_payments_by_status(
    school_id: str,
    status: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Payment.objects.filter(
        invoice__school_id=school_id,
        status=status,
    )[offset:offset + limit]


def list_payments_by_method(
    school_id: str,
    payment_method: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Payment.objects.filter(
        invoice__school_id=school_id,
        payment_method=payment_method,
    )[offset:offset + limit]