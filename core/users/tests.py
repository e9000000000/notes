from django.core.cache import caches
from rest_framework.test import APITestCase
from rest_captcha.settings import api_settings
from rest_captcha.utils import get_cache_key

from .models import CustomUser as User


cache = caches[api_settings.CAPTCHA_CACHE]


def get_auth_headers(self, username: str, password: str):
    token = self.client.post(
        f"/users/auth/", {"username": username, "password": password}, format="json"
    ).json()["token"]
    return {"HTTP_AUTHORIZATION": f"Token {token}"}


class UsersTests(APITestCase):
    def test_get_no_users(self):
        response = self.client.get("/users/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEquals(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )

    def test_create_user_wrong_captcha(self):
        response = self.client.post(
            "/users/",
            {
                "username": "u",
                "password": "1215",
                "captcha_key": "317285ae-643a-4cff-b9f5-10c2f951b0d3",
                "captcha_value": "0",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        captcha_key = self.client.post("/captcha/", format="json").json()["captcha_key"]
        cache_key = get_cache_key(captcha_key)
        captcha_value = cache.get(cache_key)
        self.assertIsNotNone(captcha_value)

        response = self.client.post(
            "/users/",
            {
                "username": "u",
                "password": "1215",
                "captcha_key": captcha_key,
                "captcha_value": captcha_value,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/users/", format="json")
        self.assertEqual(response.status_code, 200)
        data = response.json()["results"]
        self.assertEqual(len(data), 1)
        user_data = data[0]
        self.assertEqual(user_data["username"], "u")
        self.assertEqual(user_data["is_stuff"], False)
        self.assertEqual(user_data["info"], "")


class UserAuthTests(APITestCase):
    def setUp(self):
        u = User(username="u")
        u.set_password("1215")
        u.save()

    def test_user_delete_not_auth(self):
        response = self.client.delete("/users/auth/", format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_token_and_delete(self):
        # get
        response = self.client.post(
            "/users/auth/", {"username": "u", "password": "1215"}, format="json"
        )
        data = response.json()
        self.assertIn("token", data)

        # delete
        token = data["token"]
        response = self.client.delete(
            "/users/auth/", HTTP_AUTHORIZATION=f"Token {token}"
        )
        self.assertEqual(response.json(), {"success": 1})
        response = self.client.delete("/users/", HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(response.status_code, 401)


class ChangeUserPasswordTests(APITestCase):
    def setUp(self):
        self.get_auth_headers = lambda *args, **kwargs: get_auth_headers(
            self, *args, **kwargs
        )

        self.u = User(username="u", info="some info")
        self.u.set_password("1215")
        self.u.save()
        self.headers = self.get_auth_headers("u", "1215")

    def test_change_wrong_old(self):
        send_data = {"old_password": "fo3if32", "new_password": "1150"}
        response = self.client.patch(
            "/users/change_password/", send_data, **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_change_password(self):
        send_data = {"old_password": "1215", "new_password": "1150"}
        response = self.client.patch(
            "/users/change_password/", send_data, **self.headers, format="json"
        )
        self.assertEqual(response.json(), {"success": 1})

        self.u.refresh_from_db()
        self.assertTrue(self.u.check_password("1150"))

        # try delete with old token
        response = self.client.delete(
            f"/users/{self.u.pk}/", **self.headers, format="json"
        )
        self.assertEqual(response.status_code, 401)


class UserDetailsTests(APITestCase):
    def setUp(self):
        self.admin = User(username="admin", is_stuff=True)
        self.admin.set_password("1150")
        self.admin.save()

        self.another_admin = User(username="another_admin", is_stuff=True)
        self.another_admin.set_password("911")
        self.another_admin.save()

        self.u = User(username="u", info="some info")
        self.u.set_password("1215")
        self.u.save()

        self.another_u = User(username="another_u")
        self.another_u.set_password("314")
        self.another_u.save()

        self.get_auth_headers = lambda *args, **kwargs: get_auth_headers(
            self, *args, **kwargs
        )

    def test_get_user_info(self):
        response = self.client.get(f"/users/{self.u.pk}/", format="json")
        data: dict = response.json()
        self.assertEqual(
            set(data), {"id", "username", "info", "is_stuff", "registration_date"}
        )
        self.assertEqual(data["id"], self.u.pk)
        self.assertEqual(data["username"], "u")
        self.assertEqual(data["info"], "some info")
        self.assertEqual(data["is_stuff"], False)

    def test_edit_and_delete_user_no_auth(self):
        response = self.client.patch(
            f"/users/{self.u.pk}/", {"username": "uu"}, format="json"
        )
        self.assertEqual(response.status_code, 401, f"{response.json()=}")
        response = self.client.delete(f"/users/{self.u.pk}/", format="json")
        self.assertEqual(response.status_code, 401, f"{response.json()=}")

    def test_edit_and_delete_as_another_user(self):
        headers = self.get_auth_headers("another_u", "314")
        response = self.client.patch(
            f"/users/{self.u.pk}/", {"username": "uu"}, format="json", **headers
        )
        self.assertEqual(response.status_code, 403, f"{response.json()=}")
        response = self.client.delete(f"/users/{self.u.pk}/", format="json", **headers)
        self.assertEqual(response.status_code, 403, f"{response.json()=}")

    def test_edit_and_delete_admin_as_another_admin(self):
        headers = self.get_auth_headers("another_admin", "911")
        response = self.client.patch(
            f"/users/{self.admin.pk}/", {"username": "uu"}, format="json", **headers
        )
        self.assertEqual(response.status_code, 403, f"{response.json()=}")
        response = self.client.delete(
            f"/users/{self.admin.pk}/", format="json", **headers
        )
        self.assertEqual(response.status_code, 403, f"{response.json()=}")

    def test_edit_and_delete_self(self):
        headers = self.get_auth_headers("u", "1215")
        self.edit_and_delete_user_as_someone_who_have_permission(headers)

    def test_edit_and_delete_as_admin(self):
        headers = self.get_auth_headers("admin", "1150")
        self.edit_and_delete_user_as_someone_who_have_permission(headers)

    def edit_and_delete_user_as_someone_who_have_permission(self, headers):
        # edit
        response = self.client.patch(
            f"/users/{self.u.pk}/", {"username": "uu"}, format="json", **headers
        )
        self.assertEqual(response.status_code, 200, f"response.json()")
        self.u.refresh_from_db()
        self.assertEqual(self.u.username, "uu")

        response = self.client.patch(
            f"/users/{self.u.pk}/", {"info": "test info"}, format="json", **headers
        )
        self.assertEqual(response.status_code, 200, f"response.json()")
        self.u.refresh_from_db()
        self.assertEqual(self.u.info, "test info")

        response = self.client.patch(
            f"/users/{self.u.pk}/",
            {"username": "ua", "password": "aa"},
            format="json",
            **headers,
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            f"/users/{self.u.pk}/", {"is_stuff": True}, format="json", **headers
        )
        self.u.refresh_from_db()
        self.assertEqual(self.u.is_stuff, False)

        # delete
        response = self.client.delete(f"/users/{self.u.pk}/", format="json", **headers)
        self.assertEqual(response.json(), {"success": 1})
        try:
            User.objects.get(pk=self.u.pk)
            self.assertEqual(0, 1, "user is not deleted")
        except User.DoesNotExist:
            pass
        except Exception as e:
            self.assertEqual(
                0, 1, f"user is not deleted, but exception was raised {e=}"
            )
