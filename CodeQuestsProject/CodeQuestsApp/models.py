from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.utils.crypto import get_random_string
from datetime import timedelta

# Create your models here.


class Manager(BaseUserManager):

    def create_superuser(self, email, username, password, name, surname, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, name, surname, **other_fields)

    def create_user(self, email, username, password, name, surname, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, surname=surname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=80, unique=True)

    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    phone = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'name', 'surname']

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=127)
    programming_language = models.CharField(max_length=50)
    added_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    logo = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class Task(models.Model):
    name = models.CharField(max_length=80)
    text = models.CharField(max_length=500)
    ai_generated = models.BooleanField(default=False)
    correct_output = models.CharField(max_length=100)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)

    very_easy = 'V'
    easy = 'E'
    medium = 'M'
    hard = 'H'
    realy_hard = 'R'

    difficulty = [
        (very_easy, 'Very Easy'),
        (easy, 'Easy'),
        (medium, 'Medium'),
        (hard, 'Hard'),
        (realy_hard, 'Really Hard'),
    ]

    difficulty_level = models.CharField(max_length=1, choices=difficulty, default=medium)

    def __str__(self):
        return self.name


class Solution(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_code = models.CharField(max_length=1000)
    execution_time = models.IntegerField(blank=True, null=True)
    passed = models.BooleanField(default=False)
    output = models.CharField(max_length=1000, null=True, blank=True)
    match = models.ForeignKey('Match', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username + '-' + self.task.name + '-' + str(self.id)


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    condition = models.CharField(max_length=500)
    users = models.ManyToManyField(MyUser)

    def __str__(self):
        return self.name


class Match(models.Model):
    first_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='matches_as_first_user')
    second_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    has_winner = models.BooleanField(default=False)
    queued = models.BooleanField(default=True)

    def __str__(self):
        # ustimaj ovo jer ako ima prazno polje za second usera onda ovo dole ne moze ucitat username
        # return self.first_user.username + ' vs ' + self.second_user.username + ' ' + str(self.id)
        return str(self.id)


class Table(models.Model):
    name = models.CharField(max_length=25)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Ranking(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rank = models.IntegerField()
    points = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)






