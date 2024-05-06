from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    # path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.course_detail, name="course-detail"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    # path("authors/", views.AuthorListView.as_view(), name="authors"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path("students/<int:pk>", student_detail, name="student-detail"),
    # # re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    # path("borrowedbooks/", views.all_burrowed, name="all-borrowed"),
]
