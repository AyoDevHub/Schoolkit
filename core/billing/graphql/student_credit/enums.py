import strawberry

from billing.models import StudentCreditReason


StudentCreditReasonEnum = strawberry.enum(StudentCreditReason)