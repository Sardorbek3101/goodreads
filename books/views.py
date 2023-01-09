from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from books.forms import BookReviewForm
# from django.views.generic import ListView, DetailView
from books.models import Book, BookReview, Author


# class BooksView(ListView):
#     template_name = "books/list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2

class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        page_size = request.GET.get("page_size", 4)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)
        return render(request, "books/list.html", {"page_obj": page_obj, "search_query": search_query})


# class BookDetailView(DetailView):
#     template_name = "books/detail.html"
#     pk_url_kwarg = "id"
#     model = Book


class BookDetailView(View):
    def get(self, request, id):
        review_form = BookReviewForm()
        book = Book.objects.get(id=id)
        return render(request, "books/detail.html", {"book": book, "review_form": review_form})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))
        return render(request, "books/detail.html", {"book": book, "review_form": review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        return render(request, "books/edit_review.html", {"book":book, "review":review, "review_form":review_form})
    
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id":book_id}))
        
        return render(request, "books/edit_review.html", {"book":book, "review":review, "review_form":review_form})
    

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, "books/confirm_delete_review.html", {"book":book, "review":review})
    

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))
    

class AuthorsView(View):
    def get(self, request):
        authors = Author.objects.all().order_by("id")
        search = request.GET.get("q", "")
        if search:
            authors = authors.filter(first_name__icontains=search)
        page_size = request.GET.get("page_size", 4)
        paginator = Paginator(authors, page_size)
        page = request.GET.get("page", "")
        page_obj = paginator.get_page(page)
        return render(request, "books/authors.html", {"page_obj":page_obj, "search_query":search})
    

class AuthorDetailView(View):
    def get(self, request, id):
        author = Author.objects.get(id=id)
        return render(request, "books/author_detail.html", {"author":author})