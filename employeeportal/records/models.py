from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    department = models.ManyToManyField(Department)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
