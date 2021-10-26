from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reviews.models import Book, Review
from reviews.utils import average_rating


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
    return render(request, 'book-search.html', {'search_query': search_query})


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


def book_detail(request, pk, title):
    book = get_object_or_404(Book, pk=pk, title = title)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book,
                   "book_rating": book_rating,
                   "reviews": reviews,
                   "title": title}
    else:
        context = {"book": book,
                   "book_rating": None,
                   "reviews": None,
                   "title": title}
    return render(request, "reviews/book_detail.html", context)
