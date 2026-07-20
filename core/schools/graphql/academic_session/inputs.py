from datetime import date
import strawberry


@strawberry.input
class CreateAcademicSessionInput:
    school_id: strawberry.ID
    name: str
    start_date: date
    end_date: date


@strawberry.input
class UpdateAcademicSessionInput:
    session_id: strawberry.ID
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None


@strawberry.input
class ActivateAcademicSessionInput:
    session_id: strawberry.ID


@strawberry.input
class DeactivateAcademicSessionInput:
    session_id: strawberry.ID