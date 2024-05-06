from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Category(models.Model):
    """Model representing a course category (e.g. 1C - ИТ, 1C - Консалтинг)"""

    name = models.CharField(
        max_length=100,
        help_text="Категория курса (e.g. 1C - ИТ, 1C - Консалтинг)",
    )

    class Meta:
        # ordering = ["name"]
        verbose_name = "Категория"

    def __str__(self):
        return self.name


class Course(models.Model):
    """Model representing a course"""

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Краткое описание курса")
    lasting = models.IntegerField(
        default=30, help_text="Продолжительность курса, в днях"
    )
    is_selected = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    added = models.DateField(auto_now_add=True)
    rating = models.DecimalField(default=5.0, max_digits=3, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    deleted = models.DateField(auto_now=True)

    def total_cost(self):
        return (self.lasting / 30) * self.cost

    class Meta:
        ordering = ["name"]
        verbose_name = "Курс"

    def get_absolute_url(self):
        """Returns the url to access a particular course instance."""
        return reverse("course-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Mark(models.Model):
    """Model representing a mark"""

    MARKS = (
        ("1", "1 - очень плохо"),
        ("2", "2 - плохо"),
        ("3", "3 - удовлетворительно"),
        ("4", "4 - хорошо"),
        ("5", "5 - отлично"),
    )
    mark_value = models.CharField(choices=MARKS)


class Student(models.Model):
    """Model representing a student"""

    related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Имя", max_length=50)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)
    # email = models.EmailField()
    phone = models.CharField(verbose_name="Номер телефона", max_length=50)
    date_of_birth = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="photoes/", null=True, blank=True)

    STUDENT_STATUS = [
        ("r", "requested"),
        ("a", "approved"),
        ("f", "finished"),
    ]

    status = models.CharField(
        choices=STUDENT_STATUS,
        default="r",
        help_text="Статус студента",
    )
    request_date = models.DateField(auto_now_add=True)
    registered = models.DateField(blank=True, null=True)

    @property
    def is_finished(self):
        if self.registered and date.today() > self.registered + timedelta(
            self.course.lasting
        ):
            return True
        return False

    marks = models.ManyToManyField(Mark)

    def average_mark(self):
        """Creates an average for the marks. This is required to display marks in Admin."""
        mark_list = [int(mark.mark_value) for mark in self.marks.all()]
        return sum(mark_list) / len(mark_list)

    class Meta:
        ordering = ["name"]
        verbose_name = "Студент"

    def get_absolute_url(self):
        """Returns the url to access a particular student instance."""
        return reverse("student-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.name}, {self.surname}"
