from django.contrib import admin
from django.urls import path
from reviews import views

urlpatterns = [path('welcome', views.welcome, name='welcome'),
               # url mapper for views.index method
               path('', views.index),
               #path('book-search', views.search),
               path('books/', views.book_list, name='book-list'),
               path('books/<int:pk>', views.book_detail, name='book_detail'),
               path('book-search', views.book_search, name = 'book_search'),
               path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
               path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
               path('order', views.order_book, name='order_book'),
               path('publisher/<int:pk>', views.publisher_edit, name="publisher_edit"),
               path('publisher/new', views.publisher_edit, name="publisher_create"),
               ]
