from billing.models import Invoice


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_invoice_by_id(
    invoice_id: str,
) -> Invoice:
    return Invoice.objects.get(
        id=invoice_id,
    )


def get_invoice_by_number(
    invoice_number: str,
) -> Invoice:
    return Invoice.objects.get(
        invoice_number=invoice_number,
    )


def list_invoices(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Invoice.objects.filter(
        school_id=school_id,
    )[offset:offset + limit]


def list_invoices_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Invoice.objects.filter(
        student_id=student_id,
    )[offset:offset + limit]


def list_invoices_by_session(
    academic_session_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Invoice.objects.filter(
        academic_session_id=academic_session_id,
    )[offset:offset + limit]


def list_invoices_by_term(
    academic_term_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Invoice.objects.filter(
        academic_term_id=academic_term_id,
    )[offset:offset + limit]


def list_invoices_by_status(
    school_id: str,
    status: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return Invoice.objects.filter(
        school_id=school_id,
        status=status,
    )[offset:offset + limit]