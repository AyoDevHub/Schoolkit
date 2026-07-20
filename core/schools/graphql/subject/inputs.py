import strawberry


@strawberry.input
class CreateSubjectInput:
    school_id: strawberry.ID
    name: str
    level_ids: list[strawberry.ID]


@strawberry.input
class UpdateSubjectInput:
    subject_id: strawberry.ID
    name: str | None = None
    level_ids: list[strawberry.ID] | None = None