import strawberry
import strawberry_django

from people.models import Guardian
from people.graphql.guardian.enums import TitleEnum

@strawberry_django.type(Guardian)
class GuardianType:
    id: strawberry.auto
    school: strawberry.auto
    title: TitleEnum
    first_name: strawberry.auto
    last_name: strawberry.auto
    middle_name: strawberry.auto
    phone_number: strawberry.auto
    email: strawberry.auto
    home_address: strawberry.auto
    receive_sms: strawberry.auto
    receive_email: strawberry.auto
    is_active: strawberry.auto
    created_at: strawberry.auto
    updated_at: strawberry.auto

    @strawberry.field(name="fullName")
    def get_full_name(self) -> str:
        return self.full_name