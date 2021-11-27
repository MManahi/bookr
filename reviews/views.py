from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from reviews.models import Book, Review, Contributor, Publisher
from reviews.utils import average_rating
from reviews.forms import SearchForm, OrderForm, PublisherForm, ReviewForm, FileUploadForm
from django.utils import timezone

""" settings and os modules are used to serve media file uploads"""
from django.conf import settings
import os

""" messages help to send a message after object is created or edited when using redirect """
from django.contrib import messages

""" get file types using mime"""
import mimetypes


# http request in view to url mapper that shows name if the name was given in GET request
# def index(request):
#     name = request.GET.get("name") or "world"
#     return HttpResponse("Hello, {}!".format(name))


# http request in view that renders the content in template
# def index(request):
#    name = request.GET.get("name") or 'world'
#    return render(request, 'base.html', {'name': name})

def index(request):
    return render(request, 'base.html')


def search(request):
    search_query = request.GET.get("search" or "")
    return render(request, '../templates/reviews/search-results.html', {'search_query': search_query})


def welcome(request):
    # message = f"<html><h1>Welcome to Bookr!</h1><p>{Book.objects.count()} books and counting!</p></html>"
    # return HttpResponse(message)
    return render(request, 'base.html')


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,
                          'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})
    context = {
        'book_list': book_list
    }
    return render(request, 'reviews/books_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book,
                   "book_rating": book_rating,
                   "reviews": reviews}
    else:
        context = {"book": book,
                   "book_rating": None,
                   "reviews": None}
    return render(request, "reviews/book_detail.html", context)


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)
            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)
            lname_contributors = Contributor.objects.filter(last_names__icontains=search)
            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)
    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "books": books})


def order_book(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            for name, value in form.cleaned_data.items():
                print("{}: ({}) {}".format(name, type(value), value))
    else:
        form = OrderForm()
    return render(request, "reviews/book-order.html", {"method": request.method, "form": form})


def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(request, "reviews/publisher_edit.html",
                  {"method": request.method, "form": form, "instance": publisher,
                   "model_type": "Publisher"})


def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            if review is None:
                messages.success(request, "Review for \"{}\" was created.".format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" was updated.".format(book))
            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_edit.html",
                  {"method": request.method, "form": form, "instance": review,
                   "model_type": "Review", "related_instance": book,
                   "related_model_type": "Book"})


# def media_serving(request):
#     if request.method == "POST":
#         save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["file_upload"].name)
#         with open(save_path, "wb") as output_file:
#             for chunk in request.FILES["file_upload"].chunks():
#                 output_file.write(chunk)
#         messages.success(request, "File {} was uploaded successfully!".format(request.FILES["file_upload"].name))
#     return render(request, "reviews/media_serving.html")


def file_upload(request):
    if request.method == "POST":
        file_upload_form = FileUploadForm(request.POST, request.FILES)
        if file_upload_form.is_valid():
            save_path = os.path.join(settings.MEDIA_ROOT, request.FILES["file_upload"].name)
            with open(save_path, "wb") as output_file:
                for chunk in request.FILES["file_upload"].chunks():
                    output_file.write(chunk)
            messages.success(request, "File {} was uploaded successfully!".format(request.FILES["file_upload"].name))
    else:
        file_upload_form = FileUploadForm()
    return render(request, "reviews/media_serving.html", {"file_upload_form": file_upload_form})
