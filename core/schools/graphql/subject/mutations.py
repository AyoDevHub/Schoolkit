import strawberry

from schools.graphql.subject.inputs import (
    CreateSubjectInput,
    UpdateSubjectInput,
)

from schools.graphql.subject.types import SubjectType

from schools.graphql.permissions import (
    CanCreateSubject,
    CanUpdateSubject,
)

from schools.services.subject_services import (
    create_subject as create_subject_service,
    update_subject as update_subject_service,
)


@strawberry.type
class SubjectMutation:

    @strawberry.mutation(
        permission_classes=[CanCreateSubject]
    )
    def create_subject(
        self,
        input: CreateSubjectInput,
    ) -> SubjectType:
        return create_subject_service(
            school_id=input.school_id,
            name=input.name,
            level_ids=input.level_ids,
        )


    @strawberry.mutation(
        permission_classes=[CanUpdateSubject]
    )
    def update_subject(
        self,
        input: UpdateSubjectInput,
    ) -> SubjectType:
        return update_subject_service(
            subject_id=input.subject_id,
            name=input.name,
            level_ids=input.level_ids,
        )