from django.urls import path

from . import views


urlpatterns = [
    path("auth/", views.AuthView.as_view()),
    path("unauth/", views.UnAuthView.as_view()),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("register/", views.RegistrationView.as_view()),
    path(
        "self/",
        views.SelfViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "update",
                "delete": "destroy",
            }
        ),
    ),
]
