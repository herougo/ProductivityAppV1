from django.contrib import admin
from .models import (
    Epic,
    WorkflowState,
    Task,
    TaskWorkflowStates,
    TaskCompletionLog,
    Sprint,
    PastSprintMetadata
)

# Register your models here.
admin.site.register(Epic)
admin.site.register(WorkflowState)
admin.site.register(Task)
admin.site.register(TaskWorkflowStates)
admin.site.register(TaskCompletionLog)
admin.site.register(Sprint)
admin.site.register(PastSprintMetadata)
