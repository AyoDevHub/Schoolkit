import strawberry

from people.models import RelationshipType


RelationshipTypeEnum = strawberry.enum(RelationshipType)