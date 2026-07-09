from django.http import HttpRequest, HttpResponse

from strawberry.django.views import GraphQLView

from accounts.context import GraphQLContext


class SchoolKitGraphQLView(GraphQLView):
    
    def get_context(
        self,
        request: HttpRequest,
        response: HttpResponse
    ): 
        return GraphQLContext(
            request=request
        )