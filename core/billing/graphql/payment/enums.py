import strawberry

from billing.models import PaymentMethod


PaymentMethodEnum = strawberry.enum(PaymentMethod)