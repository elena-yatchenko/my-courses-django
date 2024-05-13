from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from .models import Course


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
        fields = ("username", "first_name", "email")
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
        max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    surname = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+99450 XXX XX XX"}
        ),
        help_text="Номер телефона должен начинаться со знака '+', далее код страны и номер",
    )
    date_of_birth = forms.DateField(
        initial=date.today(),
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    # course = forms.ModelChoiceField(label="Курс", queryset=Course.objects.all())
