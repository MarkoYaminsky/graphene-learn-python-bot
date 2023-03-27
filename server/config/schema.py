import graphene

from server.apps.students.queries import StudentQuery, StudentGroupQuery
from server.apps.homework.queries import HomeworkQuery, StudentHomeworkQuery
from server.apps.students.mutations import StudentMutation, StudentGroupMutation
from server.apps.homework.mutations import HomeworkMutation, StudentHomeworkMutation


class Query(StudentQuery, StudentGroupQuery, HomeworkQuery, StudentHomeworkQuery):
    pass


class Mutation(graphene.ObjectType, StudentMutation, StudentGroupMutation, HomeworkMutation, StudentHomeworkMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
