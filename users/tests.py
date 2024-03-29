from django.contrib.auth import get_user
from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                "username": "Sardorbek",
                "first_name": "Sardorbek",
                "last_name": "Olimjonov",
                "email": "oscodeer@gmail.com",
                "password": "somepassword",
            }
        )

        user = CustomUser.objects.get(username="Sardorbek")

        self.assertEqual(user.first_name, "Sardorbek")
        self.assertEqual(user.last_name, "Olimjonov")
        self.assertEqual(user.email, "oscodeer@gmail.com")
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name": "Sardorbek",
                "email": "oscodeer@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)

        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "username": "Sardorbek",
                "first_name": "Sardorbek",
                "last_name": "Olimjonov",
                "email": "invalid-email",
                "password": "somepassword",
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(
            username="Sardorbek",
            email="oscodeer@gmail.com",
        )
        user.set_password("somepassword")
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                "username": "Sardorbek",
                "first_name": "Sardorbek",
                "last_name": "Olimjonov",
                "email": "oscodeer@gmail.com",
                "password": "somepassword",
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(response, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="Sardorbek", first_name="Sardorbek")
        self.db_user.set_password("somepassword")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "Sardorbek",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "alyosha",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "Sardorbek",
                "password": "alyosha"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='Sardorbek', password="somepassword")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    # def test_login_required(self):
    #     response = self.client.get(reverse("users:profile", kwargs={"id":1}))

    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/1")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="Sardorbek31",
            first_name="Sardorbek",
            last_name="Olimjonov",
            email="oscodeer@gmail.com"
        )
        user.set_password("somepassword")
        user.save()

        self.client.login(username="Sardorbek31", password="somepassword")

        response = self.client.get(reverse("users:profile", kwargs={"id":user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="Sardorbek31", password="somepass")

        response = self.client.post(
            reverse("users:profile-edit", kwargs={"id":user.id}),
            data={
                "username": "Sardorbek3101",
                "first_name": "Sardor",
                "last_name": "Olimjonov",
                "email": "oscodeer3@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.username, "Sardorbek3101")
        self.assertEqual(user.first_name, "Sardor")
        self.assertEqual(user.email, "oscodeer3@gmail.com")
        self.assertEqual(response.url, reverse("users:profile", kwargs={"id":user.id}))