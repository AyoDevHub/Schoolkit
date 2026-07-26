import strawberry

from people.models import EnrollmentStatus


EnrollmentStatusEnum = strawberry.enum(EnrollmentStatus)