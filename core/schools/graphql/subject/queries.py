import strawberry

from schools.graphql.permissions import CanViewSubjects
from schools.graphql.subject.types import SubjectType

from schools.selectors.subject_selector import (
    get_subject_by_id,
    get_subject_by_name,
    list_subjects,
)


@strawberry.type
class SubjectQueries:

    @strawberry.field(
        permission_classes=[CanViewSubjects]
    )
    def subject(
        self,
        id: strawberry.ID,
    ) -> SubjectType | None:
        return get_subject_by_id(id)


    @strawberry.field(
        permission_classes=[CanViewSubjects]
    )
    def subject_by_name(
        self,
        school_id: strawberry.ID,
        name: str,
    ) -> SubjectType | None:
        return get_subject_by_name(
            school_id,
            name,
        )


    @strawberry.field(
        permission_classes=[CanViewSubjects]
    )
    def subjects(
        self,
        school_id: strawberry.ID,
        offset: int = 0,
        limit: int = 20,
    ) -> list[SubjectType]:
        return list_subjects(
            school_id,
            offset=offset,
            limit=limit,
        )