from django.shortcuts import render
from .models import Category, Course, Mark, Student, Payment, Review
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def main(request):
    """Функция для отображения домашней (базовой) страницы сайта"""
    categories = Category.objects.all()
    request_number = Student.objects.filter(status="r").count()
    # num_visits = request.session.get("num_visits", 0)
    # request.session["num_visits"] = num_visits + 1
    return render(
        request,
        "base.html",
        context={"categories": categories, "request_number": request_number},
    )


def courses(request, flag):
    category = Category.objects.filter(flag=flag).first()
    course_list = Course.objects.filter(category=category, is_deleted=False)
    paginator = Paginator(course_list, 2)  # Show 2 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "students_app/courses_list.html",
        context={
            "category": category,
            "page_obj": page_obj,
        },
    )
    # return redirect("/")


def students(request, status):
    student_list = Student.objects.filter(status=status, is_deleted=False)
    courses = set([student.course for student in student_list])
    paginator = Paginator(list(courses), 2)  # Show 2 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "students_app/students_list.html",
        context={"status": status, "page_obj": page_obj, "student_list": student_list},
    )


def course_detail(request, id):
    course = Course.objects.filter(pk=id, is_deleted=False).first()
    students = course.student_set.filter(status="a", is_deleted=False)
    reviews = course.review_set.all()
    course.views_num += 1
    course.save()
    return render(
        request,
        "students_app/course_detail.html",
        context={"course": course, "students": students, "reviews": reviews},
    )


def student_detail(request, id):
    student = Student.objects.filter(pk=id, is_deleted=False).first()
    payments = Payment.objects.filter(student=student)
    # print(student)
    return render(
        request,
        "students_app/student_detail.html",
        context={"student": student, "payments": payments},
    )


def logout_view(request):
    logout(request)
    return redirect("/")  # на главную страницу сайта


@login_required
def profile(request, id):
    student = Student.objects.filter(pk=id, is_deleted=False).first()
    return render(
        request,
        "students_app/profile.html",
        context={"student": student},
    )
