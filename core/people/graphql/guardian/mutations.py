import strawberry

from people.graphql.guardian.inputs import (
    ActivateGuardianInput,
    CreateGuardianInput,
    DeactivateGuardianInput,
    UpdateGuardianInput,
)
from people.graphql.guardian.types import GuardianType
from people.graphql.permissions import (
    CanActivateGuardian,
    CanCreateGuardian,
    CanDeactivateGuardian,
    CanUpdateGuardian,
)
from people.services.guardian_services import (
    activate_guardian as activate_guardian_service,
    create_guardian as create_guardian_service,
    deactivate_guardian as deactivate_guardian_service,
    update_guardian as update_guardian_service,
)


@strawberry.type
class GuardianMutation:

    @strawberry.mutation(permission_classes=[CanCreateGuardian])
    def create_guardian(
        self,
        input: CreateGuardianInput,
    ) -> GuardianType:
        return create_guardian_service(
            school_id=input.school_id,
            title=input.title.value if input.title else "",
            first_name=input.first_name,
            last_name=input.last_name,
            middle_name=input.middle_name,
            phone_number=input.phone_number,
            email=input.email,
            home_address=input.home_address,
            receive_sms=input.receive_sms,
            receive_email=input.receive_email,
        )

    @strawberry.mutation(permission_classes=[CanUpdateGuardian])
    def update_guardian(
        self,
        input: UpdateGuardianInput,
    ) -> GuardianType:
        return update_guardian_service(
            guardian_id=input.guardian_id,
            title=input.title.value if input.title else None,
            first_name=input.first_name,
            last_name=input.last_name,
            middle_name=input.middle_name,
            phone_number=input.phone_number,
            email=input.email,
            home_address=input.home_address,
            receive_sms=input.receive_sms,
            receive_email=input.receive_email,
        )

    @strawberry.mutation(permission_classes=[CanActivateGuardian])
    def activate_guardian(
        self,
        input: ActivateGuardianInput,
    ) -> GuardianType:
        return activate_guardian_service(
            guardian_id=input.guardian_id,
        )

    @strawberry.mutation(permission_classes=[CanDeactivateGuardian])
    def deactivate_guardian(
        self,
        input: DeactivateGuardianInput,
    ) -> GuardianType:
        return deactivate_guardian_service(
            guardian_id=input.guardian_id,
        )