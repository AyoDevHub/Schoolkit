import strawberry 

from accounts.graphql.queries import UserQuery
from accounts.graphql.mutations import UserMutation

from schools.graphql.school.queries import SchoolQuery
from schools.graphql.school.mutations import SchoolMutation

from schools.graphql.academic_session.queries import AcademicSessionQuery
from schools.graphql.academic_session.mutations import AcademicSessionMutation

from schools.graphql.academic_term.queries import AcademicTermQuery
from schools.graphql.academic_term.mutations import AcademicTermMutation

from schools.graphql.school_class.queries import ClassLevelQueries, ClassArmQueries
from schools.graphql.school_class.mutations import ClassLevelMutation, ClassArmMutation

from schools.graphql.subject.queries import SubjectQueries
from schools.graphql.subject.mutations import SubjectMutation
@strawberry.type
class Query(
    UserQuery,
    SchoolQuery,
    AcademicSessionQuery,
    AcademicTermQuery,
    ClassLevelQueries,
    ClassArmQueries,
    SubjectQueries,
):
    pass


@strawberry.type
class Mutation(
    UserMutation,
    SchoolMutation,
    AcademicSessionMutation,
    AcademicTermMutation,
    ClassLevelMutation,
    ClassArmMutation,
    SubjectMutation,
):
    pass


schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation
    )