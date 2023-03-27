from django.db import models


class StudentGroup(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Student(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.username
