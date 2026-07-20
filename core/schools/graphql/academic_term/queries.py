import strawberry

from schools.selectors.academic_term_selector import(
    get_term_by_id,get_term_by_name,list_terms,
    list_current_terms, list_inactive_terms,
)
from schools.graphql.academic_term.enums import TermEnum
from schools.graphql.academic_term.types import AcademicTermType
from schools.graphql.permissions import CanViewAcademicTerms


@strawberry.type
class AcademicTermQuery:

    # Single Queries
    @strawberry.field(
            permission_classes=[CanViewAcademicTerms]
    )
    def term(
        self,
        id: strawberry.ID,
    ) -> AcademicTermType | None:
        return get_term_by_id(id)

    @strawberry.field
    def term_by_name(
        self,
        session_id: strawberry.ID,
        name: TermEnum,
    ) -> AcademicTermType | None:
        return get_term_by_name(session_id, name)


    # Collection Queries
    @strawberry.field(
            permission_classes=[CanViewAcademicTerms]
    )
    def terms(
        self,
        session_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[AcademicTermType]:
        return list_terms(session_id, offset=offset, limit=limit)


    @strawberry.field(
            permission_classes=[CanViewAcademicTerms]
    )
    def current_terms(
        self,
        session_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[AcademicTermType]:
        return list_current_terms(session_id, offset=offset, limit=limit)


    @strawberry.field(
            permission_classes=[CanViewAcademicTerms]
    )
    def inactive_terms(
        self,
        session_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[AcademicTermType]:
        return list_inactive_terms(session_id, offset=offset, limit=limit)