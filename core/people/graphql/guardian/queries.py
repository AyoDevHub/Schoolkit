import strawberry

from people.graphql.guardian.types import GuardianType
from people.graphql.permissions import CanViewGuardians
from people.selectors.guardian_selectors import (
    get_guardian_by_email,
    get_guardian_by_id,
    get_guardian_by_name,
    get_guardian_by_phone_number,
    list_active_guardians,
    list_guardians,
    list_inactive_guardians,
)


@strawberry.type
class GuardianQuery:

    @strawberry.field(permission_classes=[CanViewGuardians])
    def guardian(
        self,
        id: strawberry.ID,
    ) -> GuardianType | None:
        return get_guardian_by_id(id)

    @strawberry.field(permission_classes=[CanViewGuardians])
    def guardian_by_name(
        self,
        school_id: strawberry.ID,
        first_name: str,
        last_name: str,
    ) -> GuardianType | None:
        return get_guardian_by_name(
            school_id,
            first_name,
            last_name,
        )

    @strawberry.field(permission_classes=[CanViewGuardians])
    def guardian_by_phone_number(
        self,
        school_id: strawberry.ID,
        phone_number: str,
    ) -> GuardianType | None:
        return get_guardian_by_phone_number(
            school_id,
            phone_number,
        )

    @strawberry.field(permission_classes=[CanViewGuardians])
    def guardian_by_email(
        self,
        school_id: strawberry.ID,
        email: str,
    ) -> GuardianType | None:
        return get_guardian_by_email(
            school_id,
            email,
        )

    @strawberry.field(permission_classes=[CanViewGuardians])
    def guardians(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[GuardianType]:
        return list_guardians(
            school_id,
            offset,
            limit,
        )

    @strawberry.field(permission_classes=[CanViewGuardians])
    def active_guardians(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[GuardianType]:
        return list_active_guardians(
            school_id,
            offset,
            limit,
        )

    @strawberry.field(permission_classes=[CanViewGuardians])
    def inactive_guardians(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[GuardianType]:
        return list_inactive_guardians(
            school_id,
            offset,
            limit,
        )