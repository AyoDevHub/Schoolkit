import strawberry
from django.shortcuts import get_object_or_404

from billing.graphql.payment.inputs import (
    InitializePaymentInput,
    RecordOfflinePaymentInput,
    VerifyPaymentInput,
)
from billing.graphql.payment.types import (
    PaymentType,
    PaystackInitializationResponse,
)
from billing.models import Invoice
from billing.services.payment_service import (
    process_verified_payment,
    record_offline_payment,
)
from billing.services.paystack_gateway_services import (
    initialize_payment,
)


@strawberry.type
class PaymentMutation:

    @strawberry.mutation
    def initialize_payment(
        self,
        input: InitializePaymentInput,
    ) -> PaystackInitializationResponse:

        invoice = get_object_or_404(
            Invoice,
            id=input.invoice_id,
        )

        response = initialize_payment(
            invoice=invoice,
            amount=input.amount,
            callback_url=input.callback_url,
        )

        return PaystackInitializationResponse(
            authorization_url=response["authorization_url"],
            access_code=response["access_code"],
            reference=response["reference"],
        )

    @strawberry.mutation
    def verify_payment(
        self,
        input: VerifyPaymentInput,
    ) -> PaymentType:

        return process_verified_payment(
            reference=input.reference,
        )

    @strawberry.mutation
    def record_offline_payment(
        self,
        input: RecordOfflinePaymentInput,
    ) -> PaymentType:

        invoice = get_object_or_404(
            Invoice,
            id=input.invoice_id,
        )

        return record_offline_payment(
            invoice=invoice,
            amount=input.amount,
            payment_method=input.payment_method,
            payment_date=input.payment_date,
            notes=input.notes,
        )