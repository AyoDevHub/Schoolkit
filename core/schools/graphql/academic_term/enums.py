import strawberry

from schools.models import TermName


TermEnum = strawberry.enum(TermName)