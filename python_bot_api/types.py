import graphene
from graphene_django import DjangoObjectType

from apps.homework.models import Homework, StudentHomework
from apps.students.models import Student, StudentGroup


class HomeworkType(DjangoObjectType):
    class Meta:
        model = Homework


class StudentGroupType(DjangoObjectType):
    class Meta:
        model = StudentGroup


class StudentType(DjangoObjectType):
    class Meta:
        model = Student

    homework = graphene.List(HomeworkType)

    def resolve_homework(student, info):
        homeworks = StudentHomework.objects.filter(student_id=student.telegram_id)
        homework_ids = [homework.homework_id for homework in homeworks]
        return Homework.objects.filter(id__in=homework_ids)


class StudentHomeworkType(DjangoObjectType):
    class Meta:
        model = StudentHomework

    homework = graphene.Field(HomeworkType)
    student = graphene.Field(StudentType)

    def resolve_homework(student_homework, info):
        return Homework.objects.get(id=student_homework.homework_id)

    def resolve_student(student_homework, info):
        return Student.objects.get(telegram_id=student_homework.student_id)
