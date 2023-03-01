from django.contrib import admin

from apps.homework.models import Homework, StudentHomework

admin.site.register(Homework)
admin.site.register(StudentHomework)
