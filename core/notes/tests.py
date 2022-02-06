from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from users.tests import get_auth_headers
from .models import Note


User = get_user_model()


class NotesNoAuthTests(APITestCase):
    def test_get_list(self):
        response = self.client.get("/notes/", format="json")
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        response = self.client.post("/notes/", {"text": "afeef"}, format="json")
        self.assertEqual(response.status_code, 401)


class NotesTests(APITestCase):
    def setUp(self):
        self.admin_u = User(username="admin_u", is_stuff=True)
        self.admin_u.set_password("1215")
        self.admin_u.save()
        self.u = User(username="u")
        self.u.set_password("1215")
        self.u.save()
        self.another_u = User(username="another_u")
        self.another_u.set_password("1150")
        self.another_u.save()
        self.headers = get_auth_headers(self, "u", "1215")

        self.u_note = Note(text="fw", author=self.u)
        self.u_note.save()
        self.another_u_note = Note(text="eafe", author=self.another_u)
        self.another_u_note.save()
        self.another_u_public_note = Note(
            text="public", author=self.another_u, visibility=Note.BY_URL
        )
        self.another_u_public_note.save()

    def test_get_list(self):
        response = self.client.get("/notes/", **self.headers, format="json")
        data_list = response.json()
        self.assertEqual(len(data_list), 1)

        data = data_list[0]
        self.assertEqual(data["id"], str(self.u_note.pk))
        self.assertEqual(data["author"], self.u_note.author.pk)
        self.assertEqual(data["text"], self.u_note.text)
        self.assertIn("creation_date", data)
        self.assertEqual(data["visibility"], self.u_note.visibility)

    def test_create(self):
        response = self.client.post(
            "/notes/", {"text": "feef"}, **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["author"], self.u.pk)
        self.assertEqual(data["text"], "feef")
        self.assertEqual(data["visibility"], self.u_note.visibility)

    def test_get_details_of_other_users_private_note(self):
        response = self.client.get(
            f"/notes/{self.another_u_note.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_get_details_of_other_users_public_note(self):
        response = self.client.get(
            f"/notes/{self.another_u_public_note.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        note = self.another_u_public_note
        self.assertEqual(data["id"], str(note.pk))
        self.assertEqual(data["author"], note.author.pk)
        self.assertEqual(data["text"], note.text)
        self.assertEqual(data["visibility"], note.visibility)

    def test_get_details_of_users_public_note_no_auth(self):
        response = self.client.get(
            f"/notes/{self.another_u_public_note.pk}/", format="json"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        note = self.another_u_public_note
        self.assertEqual(data["id"], str(note.pk))
        self.assertEqual(data["author"], note.author.pk)
        self.assertEqual(data["text"], note.text)
        self.assertEqual(data["visibility"], note.visibility)

    def test_get_details_of_note(self):
        response = self.client.get(
            f"/notes/{self.u_note.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        note = self.u_note
        self.assertEqual(data["id"], str(note.pk))
        self.assertEqual(data["author"], note.author.pk)
        self.assertEqual(data["text"], note.text)
        self.assertEqual(data["visibility"], note.visibility)

    def test_update_delete_other_users_public_note(self):
        response = self.client.delete(
            f"/notes/{self.another_u_public_note.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(
            f"/notes/{self.another_u_public_note.pk}/",
            {"text": "patched"},
            **self.headers,
            format="json",
        )
        self.assertEqual(response.status_code, 403)

        self.another_u_public_note.refresh_from_db()
        self.assertEqual(self.another_u_public_note.text, "public")

    def test_update_delete_note(self):
        response = self.client.patch(
            f"/notes/{self.u_note.pk}/", {"author": 12}, **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 400, response.json())

        response = self.client.patch(
            f"/notes/{self.u_note.pk}/", {"id": "aa"}, **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            f"/notes/{self.u_note.pk}/",
            {"text": "patched", "visibility": "BU"},
            **self.headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        self.u_note.refresh_from_db()
        self.assertEqual(self.u_note.text, "patched")
        self.assertEqual(self.u_note.visibility, "BU", response.json())

        response = self.client.delete(
            f"/notes/{self.u_note.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 200)

        try:
            Note.objects.get(pk=self.u_note.pk)
            self.assertIsNotNone(None, "should be deleted")
        except Note.DoesNotExist:
            pass

    def test_update_delete_private_note_as_admin(self):
        headers = get_auth_headers(self, "admin_u", "1215")
        response = self.client.patch(
            f"/notes/{self.u_note.pk}/", {"text": "patched"}, **headers, format="json"
        )
        self.assertEqual(response.status_code, 200)

        self.u_note.refresh_from_db()
        self.assertEqual(self.u_note.text, "patched")

        response = self.client.delete(
            f"/notes/{self.u_note.pk}/", **headers, format="json"
        )
        self.assertEqual(response.status_code, 200)

        try:
            Note.objects.get(pk=self.u_note.pk)
            self.assertIsNotNone(None, "should be deleted")
        except Note.DoesNotExist:
            pass
