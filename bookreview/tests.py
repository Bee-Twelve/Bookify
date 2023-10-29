from urllib.parse import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from homepage.models import CustomUser
from books.models import Books
from .models import Review

class BookReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', role='member')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpassword', role='member')
        self.book = Books.objects.create(title='Test Book', author='Test Author', genre='Test Genre',
                                         pages=200, published_year=2022, description='Test Description',
                                         thumbnail='test_thumbnail.jpg', ratings_avg=0, ratings_count=0,
                                         isbn10='1234567890', isbn13=1234567890123)
        self.review = Review.objects.create(book=self.book, user=self.user2, rating=4, comment='Good book')

    def test_book_review_view(self):
        response = self.client.get(reverse('bookreview:book_review', args=(self.book.isbn13,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookreview.html')

    def test_ajax_add_review(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('bookreview:add_review', args=(self.book.isbn13,)), urlencode({
            "book_rating": 3,
            "book_review": 'Great book!',
        }), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'status': 'success', 'code': 200, 'message': 'Review berhasil ditambahkan.'})

    def test_ajax_update_review(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(reverse('bookreview:update_review', args=(self.review.pk,)), urlencode({
            'book_rating': 3,
            'book_review': 'Not bad.'
        }), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'status': 'success', 'code': 200, 'message': 'Review berhasil diedit.'})

    def test_ajax_delete_review(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.post(reverse('bookreview:delete_review', args=(self.review.pk,)), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'status': 'success', 'code': 200, 'message': 'Review berhasil dihapus.'})
