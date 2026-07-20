import strawberry 

from schools.services.academic_term_services import (
    create_term as create_term_service,
    update_term as update_term_service,
    activate_term as activate_term_service,
    deactivate_term as deactivate_term_service,
)
from schools.graphql.academic_term.types import AcademicTermType
from schools.graphql.academic_term.inputs import (
    ActivateAcademicTermInput,
    DeactivateAcademicTermInput,
    CreateAcademicTermInput,
    UpdateAcademicTermInput,
)
from schools.graphql.permissions import (
    CanCreateAcademicTerm, CanUpdateAcademicTerm,
    CanActivateAcademicTerm, CanDeactivateAcademicTerm
)

@strawberry.type
class AcademicTermMutation:


    @strawberry.mutation(
            permission_classes=[CanCreateAcademicTerm]
    )
    def create_term(
        self,
        input: CreateAcademicTermInput
    ) -> AcademicTermType:
        return create_term_service(
            session_id=input.session_id,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date
        )
    

    @strawberry.mutation(
            permission_classes=[CanUpdateAcademicTerm]
    )
    def update_term(
        self,
        input: UpdateAcademicTermInput
    ) -> AcademicTermType:
        return update_term_service(
            term_id=input.term_id,
            start_date=input.start_date,
            end_date=input.end_date
        )
    

    @strawberry.mutation(
            permission_classes=[CanActivateAcademicTerm]
    )
    def activate_term(
        self,
        input: ActivateAcademicTermInput
    ) -> AcademicTermType:
        return activate_term_service(
            term_id=input.term_id
        )


    
    @strawberry.mutation(
            permission_classes=[CanDeactivateAcademicTerm]
    )
    def deactivate_term(
        self,
        input: DeactivateAcademicTermInput
    ) -> AcademicTermType:
        return deactivate_term_service(
            term_id=input.term_id
        )