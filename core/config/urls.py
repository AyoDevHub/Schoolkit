from django.contrib import admin
from django.urls import path
#from strawberry.django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from config.graphql import SchoolKitGraphQLView

from config.schema import schema


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", csrf_exempt(SchoolKitGraphQLView.as_view(schema=schema))),
]
