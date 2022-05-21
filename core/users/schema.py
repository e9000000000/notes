from drf_spectacular.extensions import OpenApiAuthenticationExtension

from .authentication import CookieTokenAuthentication


class CookieAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = CookieTokenAuthentication
    name = "cookie token authentication"

    def get_security_definition(self, auto_scheme):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "token",
        }
