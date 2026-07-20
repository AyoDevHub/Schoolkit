import strawberry

from schools.selectors.school_class_selector import (
    get_class_level_by_id, get_class_level_by_name,
    list_class_levels, get_class_arm_by_id,
    get_class_arm_by_name, list_class_arms
)
from schools.graphql.school_class.types import ClassLevelType, ClassArmType
from schools.graphql.permissions import CanViewSchoolClassLevel, CanViewSchoolClassArm


# -------- Class Level --------

@strawberry.type()
class ClassLevelQueries:

    @strawberry.field(
            permission_classes=[CanViewSchoolClassLevel]
    )
    def class_level(
        self,
        id: strawberry.ID
    ) -> ClassLevelType | None:
        return get_class_level_by_id(id)
    

    @strawberry.field(
            permission_classes=[CanViewSchoolClassLevel]
    )
    def class_level_by_name(
        self,
        school_id: strawberry.ID,
        name: str,
    ) -> ClassLevelType | None:
        return get_class_level_by_name(school_id,name)
    

    @strawberry.field(
            permission_classes=[CanViewSchoolClassLevel]
    )
    def class_levels(
        self,
        school_id: strawberry.ID,
        offset: int=0,
        limit: int=20,
    ) -> list[ClassLevelType]:
        return list_class_levels(school_id, offset=offset, limit=limit)
    

# -------- Class Arm --------

@strawberry.type()
class ClassArmQueries:

    @strawberry.field(
            permission_classes=[CanViewSchoolClassArm]
    )
    def class_arm(
        self,
        id: strawberry.ID
    ) -> ClassArmType | None:
        return get_class_arm_by_id(id)
    

    @strawberry.field(
            permission_classes=[CanViewSchoolClassArm]
    )
    def class_arm_by_name(
        self,
        class_level_id: strawberry.ID,
        name: str
    ) -> ClassArmType | None:
        return get_class_arm_by_name(class_level_id,name)
    

    @strawberry.field(
            permission_classes=[CanViewSchoolClassArm]
    )
    def class_arms (
        class_level_id: strawberry.ID,
        offset: int=0,
        limit: int=20,
    ) -> list[ClassArmType]:
        return list_class_arms(class_level_id, offset=offset, limit=limit)