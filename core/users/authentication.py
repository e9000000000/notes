from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed


class CookieTokenAuthentication(BaseAuthentication):
    """
    cookie token based authentication.

    clients should authenticate by passing the token key in cookie with name `token`
    example of Cookie header:
        Cookie: token=401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'CookieToken'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request: Request):
        token = request.COOKIES.get("token", "")
        if not token:
            return None
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)

    def authenticate_header(self, request: Request):
        return self.keyword
