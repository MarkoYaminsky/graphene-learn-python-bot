import graphene

from apps.students.queries import StudentQuery, StudentGroupQuery
from apps.homework.queries import HomeworkQuery, StudentHomeworkQuery
from apps.students.mutations import StudentMutation, StudentGroupMutation
from apps.homework.mutations import HomeworkMutation, StudentHomeworkMutation


class Query(StudentQuery, StudentGroupQuery, HomeworkQuery, StudentHomeworkQuery):
    pass


class Mutation(graphene.ObjectType, StudentMutation, StudentGroupMutation, HomeworkMutation, StudentHomeworkMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
