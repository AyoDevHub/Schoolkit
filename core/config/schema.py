import strawberry 

from accounts.graphql.queries import UserQuery
from accounts.graphql.mutations import UserMutation

from schools.graphql.school.queries import SchoolQuery
from schools.graphql.school.mutations import SchoolMutation

from schools.graphql.academic_session.queries import AcademicSessionQuery
from schools.graphql.academic_session.mutations import AcademicSessionMutation

from schools.graphql.academic_term.queries import AcademicTermQuery
from schools.graphql.academic_term.mutations import AcademicTermMutation

from schools.graphql.school_class.queries import ClassLevelQueries, ClassArmQueries
from schools.graphql.school_class.mutations import ClassLevelMutation, ClassArmMutation

from schools.graphql.subject.queries import SubjectQueries
from schools.graphql.subject.mutations import SubjectMutation

from people.graphql.student.queries import StudentQuery
from people.graphql.student.mutations import StudentMutation

from people.graphql.guardian.queries import GuardianQuery
from people.graphql.guardian.mutations import GuardianMutation

from people.graphql.student_guardian.queries import StudentGuardianQuery
from people.graphql.student_guardian.mutations import StudentGuardianMutation

from people.graphql.enrollment.queries import EnrollmentQuery
from people.graphql.enrollment.mutations import EnrollmentMutation

from billing.graphql.fee_item.queries import FeeItemQuery
from billing.graphql.fee_item.mutations import FeeItemMutation

from billing.graphql.fee_schedule.queries import FeeScheduleQuery
from billing.graphql.fee_schedule.mutations import FeeScheduleMutation

from billing.graphql.fee_schedule_item.queries import FeeScheduleItemQuery
from billing.graphql.fee_schedule_item.mutations import FeeScheduleItemMutation

from billing.graphql.discount.queries import DiscountQuery
from billing.graphql.discount.mutations import DiscountMutation

from billing.graphql.payment.queries import PaymentQuery
from billing.graphql.payment.mutations import PaymentMutation

from billing.graphql.invoice.mutations import InvoiceMutation
from billing.graphql.invoice.queries import InvoiceQuery

from billing.graphql.receipt.queries import ReceiptQuery
from billing.graphql.receipt.mutations import ReceiptMutation

from billing.graphql.student_credit.queries import StudentCreditQuery
from billing.graphql.student_credit.mutations import StudentCreditMutation

from billing.graphql.ledger_entry.queries import LedgerEntryQuery

from billing.graphql.webhook_event.queries import WebhookEventQuery
@strawberry.type
class Query(
    UserQuery,
    SchoolQuery,
    AcademicSessionQuery,
    AcademicTermQuery,
    ClassLevelQueries,
    ClassArmQueries,
    SubjectQueries,
    StudentQuery,
    GuardianQuery,
    StudentGuardianQuery,
    EnrollmentQuery,
    FeeItemQuery,
    FeeScheduleQuery,
    FeeScheduleItemQuery,
    DiscountQuery,
    PaymentQuery,
    InvoiceQuery,
    ReceiptQuery,
    StudentCreditQuery,
    LedgerEntryQuery,
    WebhookEventQuery,
):
    pass


@strawberry.type
class Mutation(
    UserMutation,
    SchoolMutation,
    AcademicSessionMutation,
    AcademicTermMutation,
    ClassLevelMutation,
    ClassArmMutation,
    SubjectMutation,
    StudentMutation,
    GuardianMutation,
    StudentGuardianMutation,
    EnrollmentMutation,
    FeeItemMutation,
    FeeScheduleMutation,
    FeeScheduleItemMutation,
    DiscountMutation,
    PaymentMutation,
    InvoiceMutation,
    ReceiptMutation,
    StudentCreditMutation,
):
    pass


schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation
    )