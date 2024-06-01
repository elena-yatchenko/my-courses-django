from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from .models import Course, Student, Review


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "user@mail.ru"}
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]


class RegisterStudentForm(forms.Form):
    "Форма заполняется при подаче заявки на обучение"
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Имя",
    )
    surname = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Фамилия",
    )
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+99450 XXX XX XX"}
        ),
        help_text="Номер должен начинаться со знака '+', далее код страны и номер",
        label="Номер телефона",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "examlple@mail.ru"}
        ),
        help_text="При изменении данного поля изменяется email, указанный при регистрации",
        label="Эл. почта",
    )

    date_of_birth = forms.DateField(
        initial=date.today(),
        label="Дата рождения",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    # course = forms.ModelChoiceField(label="Курс", queryset=Course.objects.all())


class PaymentForm(forms.Form):
    """Форма используется для регистрации оплаты"""

    student = forms.ModelChoiceField(
        label="Студент",
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    amount = forms.DecimalField(
        label="Сумма оплаты",
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    paid_date = forms.DateField(
        label="Дата оплаты",
        initial=date.today(),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    document = forms.FileField(
        label="Документ",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-select",
                "placeholder": "Загрузите документ об оплате",
            }
        ),
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        student = self.cleaned_data["student"]
        rest_of_payment = student.rest_of_payment()
        if amount > rest_of_payment:
            raise forms.ValidationError(
                f"Сумма оплаты превышает задолженность - {rest_of_payment}"
            )
        return amount

    def clean_paid_date(self):
        paid_date = self.cleaned_data["paid_date"]
        if paid_date > date.today():
            raise forms.ValidationError("Дата оплаты не может быть больше текущей даты")
        return paid_date


class PaymentChangeForm(forms.Form):
    """Форма используется для изменения оплаты"""

    student = forms.ModelChoiceField(
        label="Студент",
        disabled=True,
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )
    amount = forms.DecimalField(
        label="Сумма оплаты",
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    paid_date = forms.DateField(
        label="Дата оплаты",
        initial=date.today(),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    document = forms.FileField(
        label="Документ",
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-select",
                "placeholder": "Загрузите документ об оплате",
            }
        ),
    )

    def clean_paid_date(self):
        paid_date = self.cleaned_data["paid_date"]
        if paid_date > date.today():
            raise forms.ValidationError("Дата оплаты не может быть больше текущей даты")
        return paid_date


class ConfirmationForm(forms.Form):
    YES_NO_CHOICES = [(True, "Принять"), (False, "Отклонить")]
    confirm_choice = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect(attrs={"class": "checkbox inline"}),
        choices=YES_NO_CHOICES,
        required=True,
    )


class AddReviewForm(forms.Form):
    RATES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )
    text = forms.CharField(
        label="Комментарий",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Напишите пару слов о нашем курсе...",
            },
        ),
    )
    rate = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check-inline"}),
        choices=RATES,
        required=True,
    )
    # rate = forms.ChoiceField(
    #     widget=forms.RadioSelect(attrs={"class": "btn-check", "type": "radio"}),
    #     choices=RATES,
    #     required=True,
    # )


class AddMarkForm(forms.Form):
    """Форма используется для добавления оценки студенту"""

    MARKS = (
        (5, "5 - отлично"),
        (4, "4 - хорошо"),
        (3, "3 - удовлетворительно"),
        (2, "2 - плохо"),
        (1, "1 - очень плохо"),
    )

    student = forms.ModelChoiceField(
        label="Студент",
        queryset=Student.objects.all(),
        empty_label=" ----- ",
        widget=forms.Select(attrs={"class": "form-check-input"}),
    )
    mark = forms.ChoiceField(
        label="Оценка",
        widget=forms.Select(attrs={"class": "form-check-inline"}),
        choices=MARKS,
        required=True,
    )
    date_of_mark = forms.DateField(
        label="Дата",
        initial=date.today(),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    # def __init__(self, course, *args, **kwargs):
    #     super(ModelChoiceField, self).__init__(*args, **kwargs)
    #     self.fields["switch"].queryset = Book.objects.filter(owner=u)


class AddImageForm(forms.Form):
    image = forms.ImageField(
        label="Ваше фото",
        widget=forms.FileInput(
            attrs={
                "class": "form-select",
                "placeholder": "Добавьте фото",
            }
        ),
    )
