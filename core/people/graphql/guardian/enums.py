import strawberry

from people.models import Title


TitleEnum = strawberry.enum(Title)