import graphene

from apps.students.models import Student, StudentGroup
from python_bot_api.types import StudentType, StudentGroupType


class MutationWithRequestStatus:
    request_details = graphene.String()


class StudentUpdateRegisterMixin(MutationWithRequestStatus):
    class Arguments:
        telegram_id = graphene.Int()
        username = graphene.String()

    student = graphene.Field(StudentType)


class StudentRegisterMutation(graphene.Mutation, StudentUpdateRegisterMixin):
    @classmethod
    def mutate(cls, _, info, telegram_id: int, username: str):
        new_student = Student.objects.create(telegram_id=telegram_id, username=username)
        return cls(student=new_student, request_details='success')


class StudentUpdateMutation(graphene.Mutation, StudentUpdateRegisterMixin):
    @classmethod
    def mutate(cls, _, info, telegram_id: int, username: str):
        student = Student.objects.filter(telegram_id=telegram_id).first()
        student.username = username
        student.save()
        return cls(student=student, request_details='success')


class StudentGroupMutationMixin(MutationWithRequestStatus):
    group = graphene.Field(StudentGroupType)


class StudentGroupCreateMutation(graphene.Mutation, StudentGroupMutationMixin):
    class Arguments:
        group_name = graphene.String()

    @classmethod
    def mutate(cls, _, info, group_name: str):
        group_exists = StudentGroup.objects.filter(name=group_name).exists()
        if group_exists:
            return cls(group=None, request_details=f'Група з назвою {group_name} вже існує.')
        group = StudentGroup.objects.create(name=group_name)
        return cls(group=group, request_details='success')


class StudentGroupAddStudent(graphene.Mutation, StudentGroupMutationMixin):
    class Arguments:
        student_username = graphene.String()
        group_name = graphene.String()

    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, _, info, student_username: str, group_name: str):
        student = Student.objects.filter(username=student_username).first()
        group = StudentGroup.objects.filter(name=group_name).first()
        if not student:
            return cls(group=group, student=student, request_details=f"Користувача {student_username} не існує.")
        if student.group:
            return cls(group=student.group, student=student, request_details='Користувач вже має групу.')
        student.group = group
        student.save()
        return cls(group=group, student=student, request_details='success')


class StudentGroupMutation:
    create_group = StudentGroupCreateMutation.Field()
    add_student_to_group = StudentGroupAddStudent.Field()


class StudentMutation:
    register_student = StudentRegisterMutation.Field()
    update_student = StudentUpdateMutation.Field()
