import strawberry

from schools.services.school_class_services import(
    create_class_level as create_class_level_service, 
    update_class_level as update_class_level_service,
    create_class_arm as create_class_arm_service,
    update_class_arm as update_class_arm_service,
)
from schools.graphql.school_class.types import ClassLevelType, ClassArmType
from schools.graphql.school_class.inputs import (
    CreateClassLevelInput, UpdateClassLevelInput,
    CreateClassArmInput, UpdateClassArmInput,
)
from schools.graphql.permissions import(
    CanCreateSchoolClassLevel, CanUpdateSchoolClassLevel,
    CanCreateSchoolClassArm, CanUpdateSchoolClassArm
)


# -------- Class Level --------

@strawberry.type
class ClassLevelMutation:

    
    @strawberry.mutation(
            permission_classes=[CanCreateSchoolClassLevel]
    )
    def create_class_level(
        self,
        input: CreateClassLevelInput,
    ) -> ClassLevelType:
        return create_class_level_service(
            school_id=input.school_id,
            name=input.name
        )
    

    @strawberry.mutation(
            permission_classes=[CanUpdateSchoolClassLevel]
    )
    def update_class_level(
        self,
        input: UpdateClassLevelInput,
    ) -> ClassLevelType:
        return update_class_level_service(
            class_level_id=input.class_level_id,
            name=input.name
        )
    

# -------- Class Arm --------

@strawberry.type
class ClassArmMutation:


    @strawberry.mutation(
            permission_classes=[CanCreateSchoolClassArm]
    )
    def create_class_arm(
        self,
        input: CreateClassArmInput,
    ) -> ClassArmType:
        return create_class_arm_service(
            class_level_id=input.class_level_id,
            name=input.name
        )
    

    @strawberry.mutation(
            permission_classes=[CanUpdateSchoolClassArm]
    )
    def update_class_arm(
        self,
        input: UpdateClassArmInput,
    ) -> ClassArmType:
        return update_class_arm_service(
            class_arm_id=input.class_arm_id,
            name=input.name
        )
