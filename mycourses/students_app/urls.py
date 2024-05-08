from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    # path("books/", views.BookListView.as_view(), name="books"),
    path("course/<int:pk>", views.course_detail, name="course-detail"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path("courses/<slug:flag>", views.courses, name="courses"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path("students/<int:pk>", views.student_detail, name="student-detail"),
    # # re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    # path("borrowedbooks/", views.all_burrowed, name="all-borrowed"),
]
