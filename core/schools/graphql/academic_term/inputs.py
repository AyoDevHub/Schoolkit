import strawberry
from datetime import date

from schools.models import TermName


@strawberry.input
class CreateAcademicTermInput:
    session_id: strawberry.ID
    name: TermName
    start_date: date
    end_date: date


@strawberry.input
class UpdateAcademicTermInput:
    term_id: strawberry.ID
    start_date: date | None = None
    end_date: date | None = None


@strawberry.input
class ActivateAcademicTermInput:
    term_id: strawberry.ID


@strawberry.input
class DeactivateAcademicTermInput:
    term_id: strawberry.ID