import strawberry

from people.models import Gender


GenderEnum = strawberry.enum(Gender)