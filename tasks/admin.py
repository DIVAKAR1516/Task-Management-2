from django.contrib import admin

from taskmanager.tasks.models import TaskUserProfile, Task

admin.site.register(Task)
admin.site.register(TaskUserProfile)