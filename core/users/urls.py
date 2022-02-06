from django.urls import path

from . import views


urlpatterns = [
    path("auth/", views.Auth.as_view()),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("", views.RegistrationView.as_view()),
    path("self/", views.SelfDetails.as_view()),
    path("<int:pk>/", views.UserDetails.as_view()),
]
