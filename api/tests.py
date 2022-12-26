from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Sardorbek", last_name="Olimjonov", email="oscodeer@gmail.com")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username="Sardorbek", password="somepass")

    def test_book_review_detail(self):
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")

        br = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment="Very Good book!")

        response = self.client.get(reverse("api:reviews-detail", kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very Good book!")
        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], "Manga")
        self.assertEqual(response.data['book']['description'], "Manga description")
        self.assertEqual(response.data['book']['isbn'], '12345678910')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['last_name'], "Olimjonov")
        self.assertEqual(response.data['user']['username'], "Sardorbek")
        self.assertEqual(response.data['user']['email'], 'oscodeer@gmail.com')

    def test_delete_review_api(self):
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")

        br = BookReview.objects.create(stars_given=5, comment="Good book!", user=self.user, book=book)

        response = self.client.delete(reverse('api:reviews-detail', kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review_api(self):
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")
        br = BookReview.objects.create(stars_given=5, comment="Good book!", user=self.user, book=book)

        response = self.client.patch(reverse("api:reviews-detail", kwargs={"id": br.id}), data={"stars_given": 2})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 2)

    def test_put_review_api(self):
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")
        br = BookReview.objects.create(stars_given=5, comment="Good book!", user=self.user, book=book)

        response = self.client.put(reverse("api:reviews-detail", kwargs={"id": br.id}), data={
            "stars_given": 2,
            "comment": "don't good book",
            "book_id": book.id,
            "user_id": self.user.id
        })
        br = BookReview.objects.get(id=br.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, "don't good book")

    def test_post_review_api(self):
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")
        response = self.client.post(reverse('api:reviews-list'), data={
            "stars_given": 3,
            "comment": "Normal book.",
            "user_id": self.user.id,
            "book_id": book.id
        })

        review = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(review.stars_given, 3)
        self.assertEqual(review.comment, "Normal book.")
        self.assertEqual(review.user_id, self.user.id)
        self.assertEqual(review.book_id, book.id)

    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username="Somebody", last_name="Somebody")
        book = Book.objects.create(title="Manga", description="Manga description", isbn="12345678910")
        br = BookReview.objects.create(user=self.user, book=book, stars_given=4, comment="Very Good book!")
        br_two = BookReview.objects.create(user=user_two, book=book, stars_given=1, comment="Not Good!")
        response = self.client.get(reverse("api:reviews-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['results'][0]['id'], br_two.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br.comment)
