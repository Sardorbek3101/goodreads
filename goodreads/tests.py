from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Book1", description='Description1', isbn="5454665")

        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        review1 = BookReview.objects.create(user=user, book=book, stars_given=3, comment="Very good book")
        review2 = BookReview.objects.create(user=user, book=book, stars_given=3, comment="Userful book")
        review3 = BookReview.objects.create(user=user, book=book, stars_given=3, comment="Nice book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
