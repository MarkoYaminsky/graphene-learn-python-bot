from django.db import models

from apps.students.models import Student


class Homework(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=40, unique=True)
    task = models.TextField()
    deadline = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return self.topic


class StudentHomework(models.Model):
    student_id = models.IntegerField()
    homework_id = models.IntegerField()
    is_done = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    objects = models.Manager()

    def __str__(self):
        return \
            f"Student ({Student.objects.get(telegram_id=self.student_id)})" \
            f" - Homework ({Homework.objects.get(id=self.homework_id)})"
