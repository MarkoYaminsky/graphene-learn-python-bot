import graphene

from apps.homework.models import StudentHomework, Homework
from apps.students.models import Student
from python_bot_api.types import HomeworkType, StudentHomeworkType


class HomeworkQuery(graphene.ObjectType):
    homework = graphene.List(HomeworkType, telegram_id=graphene.Int())
    homework_instance = graphene.Field(HomeworkType, topic=graphene.String(), homework_id=graphene.Int())

    def resolve_homework(_, info, telegram_id=None):
        if not telegram_id:
            return Homework.objects.all()
        student = Student.objects.filter(telegram_id=telegram_id).first()
        homeworks = StudentHomework.objects.filter(student_id=student.telegram_id, is_submitted=False)
        homework_ids = [homework.homework_id for homework in homeworks]
        return Homework.objects.filter(id__in=homework_ids)

    def resolve_homework_instance(_, info, topic=None, homework_id=None):
        if topic:
            return Homework.objects.filter(topic=topic).first()
        if homework_id:
            return Homework.objects.filter(id=homework_id).first()


class StudentHomeworkQuery(graphene.ObjectType):
    submitted_homework = graphene.List(StudentHomeworkType)
    students_with_undone_homework = graphene.List(StudentHomeworkType)

    def resolve_submitted_homework(_, info):
        return StudentHomework.objects.filter(is_submitted=True, is_done=False)

    def resolve_students_with_undone_homework(_, info):
        return StudentHomework.objects.filter(is_submitted=False, is_done=False)
