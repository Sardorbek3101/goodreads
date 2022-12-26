from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description='Description1', isbn="5454665")
        book2 = Book.objects.create(title="Book2", description='Description2', isbn="4455494")
        book3 = Book.objects.create(title="Book3", description='Description3', isbn="71817157")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description='Description1', isbn="5454665")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description='Description1', isbn="5454665")
        book2 = Book.objects.create(title="Anime", description='Description2', isbn="4455494")
        book3 = Book.objects.create(title="Game", description='Description3', isbn="71817157")

        response = self.client.get(reverse("books:list") + "?q=Sport")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Anime")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Game")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Sport", description='Description1', isbn="5454665")
        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="Sardorbek31", password="somepass")

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")

    def test_required_review(self):
        book = Book.objects.create(title="Sport", description='Description1', isbn="5454665")
        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="Sardorbek31", password="somepass")

        response = self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 6,
            "comment": "Nice book"
        })

        book_reviews = book.bookreview_set.all()

        self.assertFormError(response, "review_form", "stars_given", "Ensure this value is less than or equal to 5.")
        self.assertEqual(book_reviews.count(), 0)

        response = self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 4,
            "comment": ""
        })

        self.assertEqual(book_reviews.count(), 0)
        self.assertFormError(response, "review_form", "comment", "This field is required.")

    def test_edit_review(self):
        book = Book.objects.create(title="Sport", description='Description1', isbn="5454665")
        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="Sardorbek31", password="somepass")

        review = BookReview.objects.create(user=user, book=book, stars_given=4, comment="Good book bravo.")

        self.client.post(reverse("books:edit_review", kwargs={"book_id": book.id, "review_id": review.id}), data={
            "stars_given": 5,
            "comment": "Good book masterpiece!"
        })
        review.refresh_from_db()
        self.assertEqual(review.stars_given, 5)
        self.assertEqual(review.comment, "Good book masterpiece!")

    def test_delete_review(self):
        book = Book.objects.create(title="Sport", description='Description1', isbn="5454665")
        user = CustomUser.objects.create(
            username="Sardorbek31", first_name="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        self.client.login(username="Sardorbek31", password="somepass")

        review = BookReview.objects.create(user=user, book=book, stars_given=4, comment="Good book bravo.")
        all_reviews = BookReview.objects.all()
        self.assertEqual(all_reviews.count(), 1)

        self.client.get(reverse("books:delete_review", kwargs={"book_id": book.id, "review_id": review.id}))

        self.assertEqual(all_reviews.count(), 0)