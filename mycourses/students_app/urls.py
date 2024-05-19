from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("students/<str:status>", views.students, name="students"),
    path("course/<int:id>", views.course_detail, name="course-detail"),
    path("courses/<slug:flag>", views.courses, name="courses"),
    path("student/<int:id>", views.student_detail, name="student-detail"),
    path("profile/<int:stud_id>", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path(
        "student/register/<int:course_id>",
        views.student_request,
        name="student-request",
    ),
    path(
        "student/<int:stud_id>/payment", views.student_payment, name="student-payment"
    ),
    path("student/payment", views.student_payment, name="student-payment"),
    path(
        "student/approve/<int:stud_id>", views.student_approve, name="student-approve"
    ),
    path(
        "student/archive/<int:stud_id>", views.student_archive, name="student-archive"
    ),
    path("course/<int:course_id>/mark", views.add_mark, name="add-mark"),
    path("student/photo/<int:stud_id>", views.add_photo, name="add-photo"),
]
