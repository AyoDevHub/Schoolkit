import strawberry

from schools.selectors.school_selector import (
    get_school_by_id, get_school_by_name,get_school_by_code,
    list_schools, list_active_schools, list_inactive_schools
)
from schools.graphql.school.types import SchoolType, AdminSchoolType
from schools.graphql.permissions import CanViewSchools


@strawberry.type()
class SchoolQuery:

    # Single School Queries
    @strawberry.field(
            permission_classes=[CanViewSchools]
    )
    def school(
        self,
        school_id: strawberry.ID
    ) -> AdminSchoolType | None:
        return get_school_by_id(school_id)
    

    @strawberry.field(
        permission_classes=[CanViewSchools]
    )
    def school_by_name(
        self,
        name: str
    ) -> SchoolType | None:
        return get_school_by_name(name)
    

    @strawberry.field(
        permission_classes=[CanViewSchools]
    )
    def school_by_code(
        self,
        code: str
    ) -> SchoolType | None:
        return get_school_by_code(code)
    


    # Collection Queries 
    @strawberry.field(
        permission_classes=[CanViewSchools]
    )
    def schools(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> list[AdminSchoolType]:
        return list_schools(offset=offset, limit=limit)
    

    @strawberry.field(
        permission_classes=[CanViewSchools]
    )
    def active_schools(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> list[AdminSchoolType]:
        return list_active_schools(offset=offset, limit=limit)
    
    
    @strawberry.field(
        permission_classes=[CanViewSchools]
    )
    def inactive_schools(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> list[AdminSchoolType]:
        return list_inactive_schools(offset=offset, limit=limit)
