from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    """Model representing a course category (e.g. 1C - ИТ, 1C - Консалтинг)"""

    name = models.CharField(
        max_length=100,
        help_text="Категория курса (e.g. 1C - ИТ, 1C - Консалтинг)",
    )
    flag = models.CharField(max_length=10, default="cons")

    class Meta:
        # ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    """Model representing a course"""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Краткое описание курса")
    lasting = models.IntegerField(
        default=1, help_text="Продолжительность курса, в месяцах"
    )
    is_selected = models.BooleanField(default=False)
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Стоимость в месяц, азн"
    )
    added = models.DateField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateField(auto_now=True)
    views_num = models.IntegerField(default=0)

    def total_cost(self):
        return self.lasting * self.cost

    # проверить работу функции
    def rating_count(self):
        rates = [review.rate for review in self.review_set.all()]
        rating = round(sum(rates) / len(rates), 2)
        return rating

    class Meta:
        ordering = ["-name"]
        # verbose_name = "Курс"

    def get_absolute_url(self):
        """Returns the url to access a particular course instance."""
        return reverse("course-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Student(models.Model):
    """Model representing a student"""

    related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Имя", max_length=50)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)
    # email = models.EmailField()
    phone = models.CharField(verbose_name="Номер телефона", max_length=50)
    date_of_birth = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    # photo = models.ImageField(upload_to="photoes/", null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.surname} {self.name}"

    STUDENT_STATUS = [
        ("r", "requested"),
        ("a", "approved"),
        ("f", "finished"),
    ]

    status = models.CharField(
        max_length=50,
        choices=STUDENT_STATUS,
        default="r",
        help_text="Статус студента",
    )
    request_date = models.DateField(auto_now_add=True)
    reg_date = models.DateField(blank=True, null=True)
    updated = models.DateField(auto_now=True)

    @property
    def is_finished(self):
        days = self.course.lasting * 30
        if self.reg_date and date.today() > self.reg_date + timedelta(days=days):
            return True
        return False

    # marks = models.ManyToManyField(Mark, blank=True)
    is_paid = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateField(auto_now=True)

    def average_mark(self):
        """Определяет средний балл студента"""
        mark_list = [perf.mark for perf in self.performance_set.all()]
        if mark_list:
            return round(sum(mark_list) / len(mark_list), 2)
        else:
            return "Оценок нет"

    def rest_of_payment(self):
        """определяет остаток незакрытой оплаты студента"""
        paid = sum([payment.amount for payment in self.payment_set.all()])
        rest = self.course.total_cost() - paid
        return rest

    class Meta:
        ordering = ["name"]
        # verbose_name = "Студент"

    def get_absolute_url(self):
        """Returns the url to access a particular student instance."""
        return reverse("student-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.name}, {self.surname}"


class Performance(models.Model):
    """Модель отражает показатели успеваемости студента"""

    MARKS = (
        (5, "5 - отлично"),
        (4, "4 - хорошо"),
        (3, "3 - удовлетворительно"),
        (2, "2 - плохо"),
        (1, "1 - очень плохо"),
    )
    mark = models.IntegerField(choices=MARKS)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_of_mark = models.DateField(default=timezone.now())
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.mark}"


class Payment(models.Model):
    """Model representing a payment for course"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=8, decimal_places=2)
    paid_date = models.DateField(verbose_name="Дата оплаты", default=date.today)
    document = models.FileField(upload_to="files/", null=True, blank=True)
    added = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-paid_date"]
        # verbose_name = "Оплата"
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.amount}"


class Review(models.Model):
    """Model representing a comment about course"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField(
        max_length=2000,
        help_text="Отзыв к курсу",
    )
    RATES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )
    rate = models.IntegerField(choices=RATES)
    added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["added", "-id"]
        # verbose_name = "Отзыв"

    def get_summary(self):
        words = self.text.split()
        return f'{" ".join(words[:12])}...'

    def __str__(self):
        return f"{self.rate}"


class Image(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="no_name")
    image = models.ImageField(upload_to="images/")
    added = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
