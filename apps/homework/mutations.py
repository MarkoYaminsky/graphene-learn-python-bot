import datetime

import graphene

from apps.homework.models import Homework, StudentHomework
from apps.students.models import StudentGroup, Student
from python_bot_api.types import HomeworkType


class HomeworkRelatedMutation:
    homework = graphene.Field(HomeworkType)
    request_details = graphene.String()


class HomeworkCreateMutation(graphene.Mutation, HomeworkRelatedMutation):
    class Arguments:
        topic = graphene.String()
        task = graphene.String()

    deadline = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    @classmethod
    def mutate(cls, _, info, topic: str, task: str):
        task = task.replace("'''", '"""').replace('%%', '\n')
        topic_exists = Homework.objects.filter(topic=topic)
        if topic_exists:
            return cls(homework=None, request_details=f'Домашнє завдання з темою "{topic}" вже існує.')
        new_homework = Homework.objects.create(topic=topic, task=task, deadline=cls.deadline)
        return cls(homework=new_homework, request_details='success')


class HomeworkAssignMutation(graphene.Mutation, HomeworkRelatedMutation):
    class Arguments:
        homework_topic = graphene.String()
        group_name = graphene.String()
        student_username = graphene.String()

    @classmethod
    def mutate(cls, _, info, homework_topic: str, group_name=None, student_username=None):
        homework = Homework.objects.filter(topic=homework_topic).first()
        if not homework:
            return cls(homework=homework,
                       request_details=f'Домашнього завдання з темою "{homework_topic}" не існує.')

        if group_name:
            return cls.assign_by_group_name(homework=homework, group_name=group_name)

        if student_username:
            return cls.assign_by_student_username(homework=homework, student_username=student_username)

    @staticmethod
    def assign_homework(student_id: int, homework_id: int):
        combinations_exists = StudentHomework.objects.filter(
            student_id=student_id,
            homework_id=homework_id
        )

        if not combinations_exists:
            StudentHomework.objects.create(
                student_id=student_id,
                homework_id=homework_id,
                is_done=False,
                is_submitted=False
            )

    @classmethod
    def assign_by_group_name(cls, homework: Homework, group_name: str):
        group = StudentGroup.objects.filter(name=group_name).first()
        if not group:
            return cls(homework=homework, request_details=f'Групи з назвою {group_name} не існує.')
        for student in group.student_set.all():
            cls.assign_homework(student_id=student.telegram_id, homework_id=homework.id)
        return cls(homework=homework, request_details="success")

    @classmethod
    def assign_by_student_username(cls, homework: Homework, student_username: str):
        student = Student.objects.filter(username=student_username).first()
        if not student:
            return cls(homework=homework, requst_details=f'Студента з іменем {student_username} не існує.')
        cls.assign_homework(student_id=student.telegram_id, homework_id=homework.id)
        return cls(homework=homework, request_details="success")


class HomeworkSubmitMutation(graphene.Mutation, HomeworkRelatedMutation):
    class Arguments:
        student_id = graphene.Int()
        topic = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate(cls, _, info, student_id: int, topic: str, content: str):
        homework = Homework.objects.filter(topic=topic).first()
        if not homework:
            return cls(homework=homework,
                       request_details=f'Дошманього завдання з теми "{topic}" не існує.')
        homework_pair = StudentHomework.objects.filter(student_id=student_id, homework_id=homework.id).first()
        if not homework_pair:
            return cls(homework=homework,
                       request_details=f'У Вас немає домашнього завдання з теми "{topic}."')
        homework_pair.is_submitted = True
        homework_pair.content = content.replace("'''", '"""').replace('%%', '\n')
        homework_pair.save()
        return cls(homework=homework, request_details='success')


class AcceptOrDeclineHomework:
    class Arguments:
        student_id = graphene.Int()
        homework_id = graphene.Int()


class HomeworkMarkMutation(graphene.Mutation, HomeworkRelatedMutation, AcceptOrDeclineHomework):
    @classmethod
    def mutate(cls, _, info, student_id: int, homework_id: int):
        submitted_homework = StudentHomework.objects.get(student_id=student_id, homework_id=homework_id)
        submitted_homework.is_done = True
        submitted_homework.save()

        homework = Homework.objects.get(id=homework_id)
        return cls(homework=homework, request_details='success')


class HomeworkUnsubmitMutation(graphene.Mutation, HomeworkRelatedMutation, AcceptOrDeclineHomework):
    @classmethod
    def mutate(cls, _, info, student_id: int, homework_id: int):
        submitted_homework = StudentHomework.objects.get(student_id=student_id, homework_id=homework_id)
        submitted_homework.is_submitted = False
        submitted_homework.save()

        homework = Homework.objects.get(id=homework_id)
        return cls(homework=homework, request_details = 'success')


class HomeworkMutation:
    create_homework = HomeworkCreateMutation.Field()


class StudentHomeworkMutation:
    assign_homework = HomeworkAssignMutation.Field()
    submit_homework = HomeworkSubmitMutation.Field()
    mark_homework_as_done = HomeworkMarkMutation.Field()
    decline_homework = HomeworkUnsubmitMutation.Field()
