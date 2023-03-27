from django.contrib import admin

from server.apps.students.models import Student, StudentGroup

admin.site.register(Student)
admin.site.register(StudentGroup)
