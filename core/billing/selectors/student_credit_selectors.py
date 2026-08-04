from django.db.models import Sum

from decimal import Decimal
from billing.models import StudentCredit


def _paginate(
    offset: int,
    limit: int,
):
    offset = max(offset, 0)
    limit = min(max(limit, 1), 100)

    return offset, limit


def get_student_credit_by_id(
    student_credit_id: str,
) -> StudentCredit:
    return StudentCredit.objects.get(
        id=student_credit_id,
    )


def list_student_credits(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        student__school_id=school_id,
    )[offset:offset + limit]


def list_active_student_credits(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        student__school_id=school_id,
        is_active=True,
    )[offset:offset + limit]


def list_inactive_student_credits(
    school_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        student__school_id=school_id,
        is_active=False,
    )[offset:offset + limit]


def list_student_credits_by_student(
    student_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        student_id=student_id,
    )[offset:offset + limit]


def list_student_credits_by_invoice(
    invoice_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        invoice_id=invoice_id,
    )[offset:offset + limit]


def list_student_credits_by_payment(
    payment_id: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        payment_id=payment_id,
    )[offset:offset + limit]


def list_student_credits_by_reason(
    school_id: str,
    reason: str,
    offset: int = 0,
    limit: int = 20,
):
    offset, limit = _paginate(
        offset,
        limit,
    )

    return StudentCredit.objects.filter(
        student__school_id=school_id,
        reason=reason,
    )[offset:offset + limit
    ]


def get_student_available_credit(
    student_id: str,
):
    return (
        StudentCredit.objects.filter(
            student_id=student_id,
            is_active=True,
        )
    )


def get_student_available_credit_balance(
    student_id: str,
):
    return (
        StudentCredit.objects.filter(
            student_id=student_id,
            is_active=True,
        ).aggregate(
            total=Sum("remaining_amount"),
        )["total"]
        or Decimal("0.00")
    )