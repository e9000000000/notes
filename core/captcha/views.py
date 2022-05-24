from rest_captcha.views import RestCaptchaView as OldRestCaptchaView
from rest_captcha.serializers import ImageSerializer
from drf_spectacular.views import extend_schema


class RestCaptchaView(OldRestCaptchaView):
    @extend_schema(
        tags=["captcha"],
        summary="get captcha image",
        description="solve captcha, then send solution and captcha key to any other endpoint,\
            where captcha is required",
        request=None,
        responses=ImageSerializer,
    )
    def post(self, request):
        return super().post(request)
