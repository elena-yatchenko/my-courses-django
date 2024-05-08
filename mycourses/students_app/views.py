from django.shortcuts import render
from .models import Category, Course, Mark, Student, Payment, Review
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.


def main(request):
    """Функция для отображения домашней (базовой) страницы сайта"""
    categories = Category.objects.all()
    # num_visits = request.session.get("num_visits", 0)
    # request.session["num_visits"] = num_visits + 1
    return render(request, "base.html", context={"categories": categories})


def courses(request, flag):
    category = Category.objects.filter(flag=flag).first()
    course_list = Course.objects.filter(category=category)

    return render(
        request,
        "students_app/courses_list.html",
        context={"course_list": course_list, "category": category},
    )
    # return redirect("/")


def course_detail(request, pk):
    course = Course.objects.filter(pk=pk).first()
    students = course.student_set.filter(status="a")
    return render(
        request,
        "students_app/course_detail.html",
        context={"course": course, "students": students},
    )


def student_detail(request, pk):
    pass


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        "catalog/index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            "num_visits": num_visits,
        },
    )
