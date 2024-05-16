from django.core.files.storage import FileSystemStorage
from .forms import PaymentForm
from .forms import RegisterUserForm, RegisterStudentForm
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Category, Course, Mark, Student, Payment, Review
from django.contrib.auth import logout, login
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
        context={"status": status, "page_obj": page_obj,
                 "student_list": student_list},
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
def profile(request):
    student = Student.objects.filter(related_user=request.user).first()
    return render(
        request,
        "students_app/profile.html",
        context={"student": student},
    )


""" Представления для работы с формами обработки данных"""


def register(request):
    if request.method == "POST":
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            # Создаем пользователя, но не сохраняем
            new_user = user_form.save(commit=False)
            # Устанавливаем пароль (с шифрованием)
            new_user.set_password(user_form.cleaned_data["password"])
            # сохраняем пользователя в БД
            new_user.save()
            # login(request, new_user)
            return render(
                request,
                "students_app/register_done.html",
                {"user_form": user_form},
            )
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        user_form = RegisterUserForm()
        message = "Заполните поля формы"
    return render(
        request,
        "students_app/register.html",
        {"user_form": user_form, "message": message},
    )


@login_required
def student_request(request, course_id):
    current_user = request.user
    if request.method == "POST":
        course = Course.objects.filter(pk=course_id).first()
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            student = Student(
                name=cd["name"],
                surname=cd["surname"],
                phone=cd["phone"],
                date_of_birth=cd["date_of_birth"],
                course=course,
                status="r",
                related_user=current_user,
            )
            student.save()
            current_user.last_name = cd["surname"]
            current_user.save()
            return redirect("profile")
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        form = RegisterStudentForm(initial={"name": current_user.first_name})
        message = "Заполните поля формы"

    return render(
        request,
        "students_app/student_form.html",
        {"form": form, "message": message},
    )


def student_payment(request, stud_id=None):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            amount = payment_form.cleaned_data['amount']
            student = payment_form.cleaned_data['student']
            paid_date = payment_form.cleaned_data['paid_date']
            document = payment_form.cleaned_data['document']
            if document:
                fs = FileSystemStorage()
                fs.save(document.name, document)
            payment = Payment(amount=amount, student=student,
                              paid_date=paid_date, document=document)
            payment.save()
            # проверка и автообновление атрибута is_paid студента
            if student.rest_of_payment() == 0:
                student.is_paid = True
                student.save()
            return redirect('student-detail', student.pk)
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        if stud_id is not None:
            initial_student = Student.objects.filter(pk=stud_id).first()
            payment_form = PaymentForm(initial={"student": initial_student})
        else:
            payment_form = PaymentForm()
        message = "Заполните поля формы"

    return render(
        request,
        "students_app/payment_form.html",
        {"form": payment_form, "message": message},
    )

    pass
