import strawberry
from decimal import Decimal

from billing.graphql.payment.enums import PaymentMethodEnum


@strawberry.input
class InitializePaymentInput:
    invoice_id: strawberry.ID
    amount: Decimal
    callback_url: str


@strawberry.input
class VerifyPaymentInput:
    reference: str


@strawberry.input
class RecordOfflinePaymentInput:
    invoice_id: strawberry.ID
    amount: Decimal
    payment_method: PaymentMethodEnum
    payment_date: str
    refrerence: str = ""
    notes: str = ""