import strawberry 


@strawberry.input
class CreateSchoolInput:
    name: str
    code: str
    email: str
    phone_number: str = ""
    address: str = ""
    website: str = ""
    motto: str = ""
    logo=None


@strawberry.input 
class UpdateSchoolInput:
    school_id: strawberry.ID
    name: str | None = None
    code: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    website: str | None = None
    motto: str | None = None
    logo: str | None = None


@strawberry.input 
class ActivateSchoolInput:
    school_id : strawberry.ID


@strawberry.input 
class DeactivateSchoolInput:
    school_id : strawberry.ID



