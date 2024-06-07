from django.core.files.storage import FileSystemStorage
from .forms import PaymentForm, ConfirmationForm, AddReviewForm, AddImageForm
from .forms import RegisterUserForm, RegisterStudentForm, AddMarkForm, PaymentChangeForm
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Category, Course, Student, Payment, Review, Performance

# from .models import image_storage
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from datetime import date, datetime
from django.core.exceptions import ValidationError


def main(request):
    """Функция для отображения домашней (базовой) страницы сайта"""
    categories = Category.objects.all()
    request_number = Student.objects.filter(status="r").count()
    if request.user.is_authenticated:
        current_user = request.user
        current_student = (
            current_user.student_set.exclude(is_deleted=True)
            .exclude(status="f")
            .first()
        )
    else:
        current_student = None
    return render(
        request,
        "base.html",
        context={
            "categories": categories,
            "request_number": request_number,
            "student": current_student,
        },
    )


def contacts(request):
    """Отображение контактов организации"""
    return render(request, "students_app/contacts.html")


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
    user = request.user
    course = Course.objects.filter(pk=id, is_deleted=False).first()
    students = course.student_set.filter(status="a", is_deleted=False)
    reviews = course.review_set.all()
    course.views_num += 1
    course.save()
    context = {
        "course": course,
        "students": students,
        "reviews": reviews,
    }
    if user.has_perm('students_app.add_review') or user.has_perm('students_app.change_review'):
        if request.method == "POST":
            review_form = AddReviewForm(request.POST)
            if review_form.is_valid():
                user = request.user
                student = Student.objects.filter(related_user=user).first()
                cd = review_form.cleaned_data
                new_review = Review(
                    student=student, course=course, text=cd["text"], rate=cd["rate"]
                )
                new_review.save()
                course.rating = course.rating_count()
                course.save()
                return redirect("course-detail", course.id)
            # else:
            #     !!!Добавить логирование
        else:
            review_form = AddReviewForm()
        context = {
            "course": course,
            "students": students,
            "reviews": reviews,
            "form": review_form,
        }
    return render(
        request,
        "students_app/course_detail.html",
        context,
    )


def student_detail(request, id):
    student = Student.objects.filter(pk=id, is_deleted=False).first()
    payments = Payment.objects.filter(student=student)
    # image = Image.objects.filter(student=student).first()
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
    current_user = request.user
    # student = current_user.student_set.first()
    students = current_user.student_set.all()
    stud_pay = {}
    for student in students:
        # data = []
        # image = Image.objects.filter(student=student).first()
        # stud_image[student] = image
        payments = Payment.objects.filter(student=student)
        stud_pay[student] = payments

    visit_date = request.session.get("visit_date", None)
    print(f"request - {request.session}")
    print(f"visit date = {visit_date}")
    print(type(visit_date))
    if visit_date is None:
        visit_date_current = date.today()
    else:
        visit_date_current = datetime.strptime(visit_date, "%Y-%m-%d")
    print(type(visit_date_current))
    print(visit_date_current)
    """переводим дату во формат строки для добавления в сессии 
    (иначе будет ошибка Object of type date is not JSON serializable),
    а для вывода на страницу, переводим обратно в строку"""
    visit_date_new = date.today().strftime("%Y-%m-%d")
    request.session["visit_date"] = visit_date_new
    print(f"перевод в строку - {visit_date_new}")
    print(type(visit_date_new))
    print(f'новая дата посещения в сессии - {request.session["visit_date"]}')

    return render(
        request,
        "students_app/profile.html",
        context={"stud_pay": stud_pay, "visit_date": visit_date_current},
    )
    # return render(
    #     request,
    #     "students_app/profile.html",
    #     context={"student": student, "image": image,
    #              "visit_date": visit_date, 'payments': payments},
    # )


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
                {"user_form": user_form, "new_user": new_user},
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
    course = Course.objects.filter(pk=course_id).first()
    if current_user.student_set.filter(course=course, status="a"):
        return HttpResponse(
            "<h2>Похоже, вы уже обучаетесь на этом курсе в настоящее время</h2>"
        )
    elif current_user.student_set.filter(course=course, status="r"):
        return HttpResponse(
            "<h2>Похоже, вы уже подали заявку на обучение на этом курсе</h2>"
        )
    else:
        if request.method == "POST":
            form = RegisterStudentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                name = cd["name"]
                surname = cd["surname"]
                email = cd["email"]
                student = Student(
                    name=name,
                    surname=surname,
                    phone=cd["phone"],
                    date_of_birth=cd["date_of_birth"],
                    course=course,
                    status="r",
                    related_user=current_user,
                )
                student.save()
                current_user.last_name = surname
                current_user.first_name = name
                current_user.email = email
                current_user.save()
                return redirect("profile")
            else:
                # !!!! добавить ЛОГИРОВАНИЕ
                message = "Некорректные данные"
        else:
            form = RegisterStudentForm(
                initial={
                    "name": current_user.first_name,
                    "surname": current_user.last_name,
                    "email": current_user.email,
                }
            )
            message = "Заявка на обучение"

    return render(
        request,
        "students_app/student_form.html",
        {"form": form, "message": message},
    )


def student_update(request, stud_id):
    current_user = request.user
    student = Student.objects.filter(pk=stud_id).first()
    if request.method == "POST":
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd["name"]
            surname = cd["surname"]
            email = cd["email"]
            phone = cd["phone"]
            student.name = name
            student.surname = surname
            student.phone = phone
            student.save()
            current_user.last_name = surname
            current_user.first_name = name
            current_user.email = email
            current_user.save()
            return redirect("profile")
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        form = RegisterStudentForm(
            initial={
                "name": student.name,
                "surname": student.surname,
                "email": current_user.email,
                "phone": student.phone,
                "date_of_birth": student.date_of_birth,
            }
        )
        message = "Внесите необходимые изменения"

    return render(
        request,
        "students_app/student_form.html",
        {"form": form, "message": message},
    )


@permission_required("students_app.add_payment")
@permission_required("students_app.change_payment")
def student_payment(request, stud_id=None):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST, request.FILES)
        if payment_form.is_valid():
            amount = payment_form.cleaned_data["amount"]
            student = payment_form.cleaned_data["student"]
            paid_date = payment_form.cleaned_data["paid_date"]
            document = payment_form.cleaned_data["document"]
            # if document:
            #     fs = FileSystemStorage()
            #     fs.save(document.name, document)
            payment = Payment(
                amount=amount, student=student, paid_date=paid_date, document=document
            )
            payment.save()
            # проверка и автообновление атрибута is_paid студента
            if student.rest_of_payment() == 0:
                student.is_paid = True
                student.save()
            return redirect("student-detail", student.pk)
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        if stud_id is not None:
            initial_student = Student.objects.filter(pk=stud_id).first()
            payment_form = PaymentForm(
                initial={
                    "student": initial_student,
                    "amount": initial_student.rest_of_payment(),
                }
            )
        else:
            payment_form = PaymentForm()
        message = "Заполните поля формы"

    return render(
        request,
        "students_app/payment_form.html",
        {"form": payment_form, "message": message},
    )


@permission_required("students_app.add_payment")
@permission_required("students_app.change_payment")
def payment_update(request, stud_id, pay_id):
    student = Student.objects.filter(pk=stud_id).first()
    payment = Payment.objects.filter(pk=pay_id).first()
    if request.method == "POST":
        payment_change_form = PaymentChangeForm(request.POST, request.FILES)
        if payment_change_form.is_valid():
            amount_before = payment.amount
            amount = payment_change_form.cleaned_data["amount"]
            payment.amount = amount
            paid_date = payment_change_form.cleaned_data["paid_date"]
            payment.paid_date = paid_date
            document = payment_change_form.cleaned_data["document"]
            if document:
                # fs = FileSystemStorage()
                # fs.save(document.name, document)
                payment.document = document
            payment.save()
            rest_of_payment = student.rest_of_payment()
            if rest_of_payment < 0:
                payment.amount = amount_before
                payment.save()
                message = "Сумма оплаты превышает задолженность!"
                return render(
                    request,
                    "students_app/error.html",
                    {"student": student, "message": message},
                )
            elif rest_of_payment == 0:
                student.is_paid = True
                student.save()
            else:
                student.is_paid = False
                student.save()
            return redirect("student-detail", stud_id)
        else:
            # !!!! добавить ЛОГИРОВАНИЕ
            message = "Некорректные данные"
    else:
        payment_change_form = PaymentChangeForm(
            initial={
                "student": student,
                "amount": payment.amount,
                "paid_date": payment.paid_date,
            }
        )
        # payment_form.fields["student"].disabled = True
        message = "Внесите требуемые изменения"

    return render(
        request,
        "students_app/payment_form.html",
        {"form": payment_change_form, "message": message},
    )


@staff_member_required
def student_approve(request, stud_id):
    # back_url = request.path
    back_url = request.GET["next"]
    student = Student.objects.filter(pk=stud_id, is_deleted=False).first()
    if request.method == "POST":
        confirm_form = ConfirmationForm(request.POST)
        if confirm_form.is_valid():
            confirm_choice = confirm_form.cleaned_data["confirm_choice"]
            if confirm_choice == "False":
                return redirect(back_url)
            else:
                user = student.related_user
                group = Group.objects.get(name="Students")
                user.groups.add(group)
                student.status = "a"
                student.reg_date = date.today()
                student.save()
                return redirect("student-detail", stud_id)

        else:
            message = "Некорректные данные"
    else:
        confirm_form = ConfirmationForm()
        message = "Подтверждение заявки на обучение студента: "
    return render(
        request,
        "students_app/confirmation.html",
        {"form": confirm_form, "message": message, "student": student},
    )


@staff_member_required
def student_archive(request, stud_id):
    # получаем из GET запроса путь к странице, с которой запущена данная функция-представление
    back_url = request.GET["next"]
    student = Student.objects.filter(pk=stud_id, is_deleted=False).first()
    if request.method == "POST":
        confirm_form = ConfirmationForm(request.POST)
        if confirm_form.is_valid():
            confirm_choice = confirm_form.cleaned_data["confirm_choice"]
            if confirm_choice == "False":
                return redirect(back_url)
            else:
                """перемещение пользователя из группы доступа Students в группу Archived происходит только
                 в том случае, если только студент не обучается на других курсах. Иначе просто меняем статус
                 с approved на finished"""
                user = student.related_user
                students = Student.objects.filter(
                    related_user=user, is_deleted=False)
                if len(students) == 1:
                    group_for_add, created = Group.objects.get_or_create(
                        name="Archive")
                    group_for_delete = Group.objects.get(name="Students")
                    user.groups.add(group_for_add)
                    user.groups.remove(group_for_delete)
                student.status = "f"
                student.save()

                return redirect("student-detail", stud_id)

        else:
            message = "Некорректные данные"
    else:
        confirm_form = ConfirmationForm()
        message = "Добавление в архив студента: "
    return render(
        request,
        "students_app/confirmation.html",
        {"form": confirm_form, "message": message, "student": student},
    )


@permission_required("students_app.add_performance")
@permission_required("students_app.change_performance")
def add_mark(request, course_id):
    """Добавляем оценку студента"""
    back_url = request.GET["next"]
    course = Course.objects.filter(pk=course_id).first()
    """переопределяем queryset, чтобы давался список не всех студентов, а только выбранного курса"""
    switch_query = Student.objects.filter(course=course, status="a")
    current_date = date.today()
    if request.method == "POST":
        add_form = AddMarkForm(request.POST)
        if add_form.is_valid():
            cd = add_form.cleaned_data
            mark = cd["mark"]
            student = cd["student"]
            date_of_mark = cd["date_of_mark"]
            performance = Performance(
                student=student, mark=mark, date_of_mark=date_of_mark
            )
            performance.save()
            message = f"Оценка для студента {student.full_name} добавлена успешно."
            add_form = AddMarkForm()
            add_form.fields["student"].queryset = switch_query
            # return redirect(back_url)
        else:
            message = "Некорректные данные"
    else:
        add_form = AddMarkForm()
        add_form.fields["student"].queryset = switch_query
        message = "Выберите студента и добавьте оценку. Вы можете выставлять оценки различным \
            студентам данного курса, каждый раз нажимая кнопку 'Подтвердить'"
    return render(
        request,
        "students_app/mark_form.html",
        {
            "form": add_form,
            "message": message,
            "current_date": current_date,
            "course": course,
            "back_url": back_url,
        },
    )


def add_photo(request, stud_id):
    student = Student.objects.filter(pk=stud_id).first()
    if request.method == "POST":
        image_form = AddImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data["image"]
            # fs = FileSystemStorage()
            # fs.save(image.name, image)
            student.photo = image
            student.save()
            # return redirect("profile")
            return render(
                request,
                "students_app/photo.html",
                context={"image": student.photo, "form": image_form},
            )
    else:
        image_form = AddImageForm()
    return render(
        request,
        "students_app/photo.html",
        context={"form": image_form},
    )
