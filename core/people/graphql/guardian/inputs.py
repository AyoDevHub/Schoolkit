from datetime import datetime

import strawberry

from people.graphql.guardian.enums import TitleEnum


@strawberry.input
class CreateGuardianInput:
    school_id: strawberry.ID
    title: TitleEnum | None = None
    first_name: str
    last_name: str
    middle_name: str = ""
    phone_number: str
    email: str = ""
    home_address: str = ""
    receive_sms: bool = True
    receive_email: bool = True


@strawberry.input
class UpdateGuardianInput:
    guardian_id: strawberry.ID
    title: TitleEnum | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    home_address: str | None = None
    receive_sms: bool | None = None
    receive_email: bool | None = None


@strawberry.input
class ActivateGuardianInput:
    guardian_id: strawberry.ID


@strawberry.input
class DeactivateGuardianInput:
    guardian_id: strawberry.ID