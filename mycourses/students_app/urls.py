from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("students/<str:status>", views.students, name="students"),
    path("course/<int:id>", views.course_detail, name="course-detail"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path("courses/<slug:flag>", views.courses, name="courses"),
    # # re_path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path("student/<int:id>", views.student_detail, name="student-detail"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path(
        "student/register/<int:course_id>",
        views.student_request,
        name="student-request",
    ),
    path("student/<int:stud_id>/payment",
         views.student_payment, name="student-payment"),
    path("student/payment", views.student_payment, name="student-payment"),
    # # re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    # path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    # path("borrowedbooks/", views.all_burrowed, name="all-borrowed"),
]
