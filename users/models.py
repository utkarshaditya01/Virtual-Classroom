from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = False
    is_tutor = False

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"


class Tutor(User):
    is_tutor = True

    class Meta:
        verbose_name = "Tutor"


class Student(User):
    is_student = True

    class Meta:
        verbose_name = "Student"
