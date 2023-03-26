import graphene
from apps.students.models import Student, StudentGroup
from python_bot_api.types import StudentType, StudentGroupType


class StudentQuery(graphene.ObjectType):
    students = graphene.List(StudentType, group_name=graphene.String())
    student = graphene.Field(StudentType, telegram_id=graphene.Int(), username=graphene.String())

    def resolve_students(_, info, group_name=None):
        if group_name:
            return Student.objects.filter(group__name=group_name)
        return Student.objects.all()

    def resolve_student(_, info, telegram_id: int = None, username: str = None):
        if telegram_id:
            student = Student.objects.filter(telegram_id=telegram_id).first()
        elif username:
            student = Student.objects.filter(username=username).first()
        else:
            return
        return student


class StudentGroupQuery(graphene.ObjectType):
    groups = graphene.List(StudentGroupType, student_id=graphene.Int())
    group = graphene.Field(StudentGroupType, name=graphene.String())

    def resolve_groups(_, info, student_id=None):
        if not student_id:
            return StudentGroup.objects.all()
        student = Student.objects.filter(telegram_id=student_id).first()
        if student:
            return student.group

    def resolve_group(_, info, name: str = None):
        if name:
            return StudentGroup.objects.filter(name=name).first()
        return
