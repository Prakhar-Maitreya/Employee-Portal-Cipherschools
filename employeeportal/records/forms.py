from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Employee
from .models import Department


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
