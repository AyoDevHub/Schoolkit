import strawberry 

from schools.graphql.school.inputs import (
    CreateSchoolInput, UpdateSchoolInput,
    ActivateSchoolInput, DeactivateSchoolInput,
)
from schools.graphql.school.types import AdminSchoolType
from schools.services.school_services import (
    create_school as create_school_service,
    update_school as update_school_service,
    activate_school as activate_school_service,
    deactivate_school as deactivate_school_service,
)
from schools.graphql.permissions import(
    CanCreateSchool, CanDeactivateSchool, CanUpdateSchool, CanActivateSchool
)



@strawberry.type
class SchoolMutation:

    @strawberry.mutation(
            permission_classes=[CanCreateSchool]
    )
    def create_school(
        self,
        input: CreateSchoolInput
    ) -> AdminSchoolType:
        return create_school_service(
            name=input.name,
            code=input.code,
            email=input.email,
            phone_number=input.phone_number,
            address=input.address,
            website=input.website,
            motto=input.motto,
            logo=input.logo,
        )
    


    @strawberry.mutation(
        permission_classes=[CanUpdateSchool]
    )
    def update_school(
        self,
        input: UpdateSchoolInput
    ) -> AdminSchoolType:
        return update_school_service(
            school_id=input.school_id,
            name=input.name,
            code=input.code,
            email=input.email,
            phone_number=input.phone_number,
            address=input.address,
            website=input.website,
            motto=input.motto,
            logo=input.logo,
        )
    

    @strawberry.mutation(
            permission_classes=[CanActivateSchool]
    )
    def activate_school(
        self,
        input: ActivateSchoolInput
    ) -> AdminSchoolType:
        return activate_school_service(
            school_id=input.school_id
        )
    

    @strawberry.mutation(
            permission_classes=[CanDeactivateSchool]
    )
    def deactivate_school(
        self,
        input: DeactivateSchoolInput
    ) -> AdminSchoolType:
        return deactivate_school_service(
            school_id=input.school_id
        )