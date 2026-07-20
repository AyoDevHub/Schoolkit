import strawberry

from schools.selectors.academic_session_selector import (
    get_session_by_id, get_session_by_name,
    list_sessions, list_current_sessions, list_inactive_sessions
)
from schools.graphql.academic_session.types import AcademicSessionType
from schools.graphql.permissions import CanViewAcademicSessions

@strawberry.type()
class AcademicSessionQuery:

    # Single Queries
    @strawberry.field(
            permission_classes=[CanViewAcademicSessions]
    )
    def session(
        self,
        id : strawberry.ID
    ) -> AcademicSessionType | None:
        return get_session_by_id(id)
    

    @strawberry.field(
            permission_classes=[CanViewAcademicSessions]
    )
    def session_by_name(
        self,
        id: strawberry.ID,
        name: str
    ) -> AcademicSessionType | None:
        return get_session_by_name(id, name)
    

    # Collection Queries
    @strawberry.field(
        permission_classes=[CanViewAcademicSessions]
    )
    def sessions(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20
    ) -> list[AcademicSessionType]:
        return list_sessions(school_id, offset=offset, limit=limit)
    

    @strawberry.field(
            permission_classes=[CanViewAcademicSessions]
    )
    def current_sessions(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20
    ) -> list[AcademicSessionType]:
        return list_current_sessions(school_id, offset=offset, limit=limit)
    

    @strawberry.field(
            permission_classes=[CanViewAcademicSessions]
    )
    def inactive_sessions(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20
    ) -> list[AcademicSessionType]:
        return list_inactive_sessions(school_id, offset=offset, limit=limit)