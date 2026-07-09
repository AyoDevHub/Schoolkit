from dataclasses import dataclass
from functools import cached_property

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()


@dataclass
class GraphQLContext:
    request: HttpRequest

    @cached_property
    def user(self):
        authentication = JWTAuthentication()

        try:
            result = authentication.authenticate(self.request)
        except (InvalidToken, TokenError):
            return None

        if result is None:
            return None

        user, _ = result

        return user