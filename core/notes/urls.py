from django.urls import path

from .views import NotesView, NoteDetailsView


urlpatterns = [
    path("", NotesView.as_view()),
    path("<str:pk>/", NoteDetailsView.as_view()),
]
