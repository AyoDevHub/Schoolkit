import strawberry 

from schools.graphql.academic_session.types import AcademicSessionType
from schools.services.academic_session_services import (
    create_session as create_session_service,
    update_session as update_session_service,
    activate_session as activate_session_service,
    deactivate_session as deactivate_session_service,
)
from schools.graphql.academic_session.inputs import (
    CreateAcademicSessionInput, UpdateAcademicSessionInput,
    ActivateAcademicSessionInput, DeactivateAcademicSessionInput,
)
from schools.graphql.permissions import(
    CanCreateAcademicSession, CanUpdateAcademicSession,
      CanActivateAcademicSession, CanDeactivateAcademicSession,
)


@strawberry.type
class AcademicSessionMutation:


    @strawberry.mutation(
            permission_classes=[CanCreateAcademicSession]
    )
    def create_session(
        self,
        input: CreateAcademicSessionInput
    ) -> AcademicSessionType:
        return create_session_service(
            school_id=input.school_id,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
        )
    

    @strawberry.mutation(
            permission_classes=[CanUpdateAcademicSession]
    )
    def update_session(
        self,
        input: UpdateAcademicSessionInput
    ) -> AcademicSessionType:
        return update_session_service(
            session_id=input.session_id,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
        )


    @strawberry.mutation(
            permission_classes=[CanActivateAcademicSession]
    )
    def activate_session(
        self,
        input: ActivateAcademicSessionInput
    ) -> AcademicSessionType:
        return activate_session_service(
            session_id=input.session_id,
        )


    @strawberry.mutation(
            permission_classes=[CanDeactivateAcademicSession]
    )
    def deactivate_session(
        self,
        input: DeactivateAcademicSessionInput
    ) -> AcademicSessionType:
        return deactivate_session_service(
            session_id=input.session_id,
        )


