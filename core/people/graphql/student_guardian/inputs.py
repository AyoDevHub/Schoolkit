import strawberry

from people.graphql.student_guardian.enums import RelationshipTypeEnum


@strawberry.input
class CreateStudentGuardianInput:
    student_id: strawberry.ID
    guardian_id: strawberry.ID
    relationship: RelationshipTypeEnum
    is_primary: bool = False


@strawberry.input
class UpdateStudentGuardianInput:
    student_guardian_id: strawberry.ID
    relationship: RelationshipTypeEnum | None = None
    is_primary: bool | None = None


@strawberry.input
class ActivateStudentGuardianInput:
    student_guardian_id: strawberry.ID


@strawberry.input
class DeactivateStudentGuardianInput:
    student_guardian_id: strawberry.ID