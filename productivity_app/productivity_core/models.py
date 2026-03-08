from django.db import models
from django.contrib.auth.models import User


class Epic(models.Model):
    """
    Groups related tasks together.
    Each epic belongs to a user and has a name, display name, and color.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='epics')
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    colour = models.CharField(max_length=7)  # Hex color code (e.g., #FF5733)
    date_created = models.DateTimeField(auto_now_add=True)


class WorkflowState(models.Model):
    """
    Represents task statuses (e.g., Backlog, In Progress, Done).
    Each state has an order for sequencing and flags for board display and completion.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflow_states')
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    is_on_board = models.BooleanField()
    is_final = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'order'], name='unique_user_order')
        ]


class Sprint(models.Model):
    """
    Represents week-long sprints for organizing work.
    Each sprint has a start and end date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sprints')
    start_date = models.DateField()
    end_date = models.DateField()


class Task(models.Model):
    """
    Core entity representing a unit of work.
    Each task has a status, can belong to an epic and sprint, and tracks creation/update times.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    current_status = models.ForeignKey(
        WorkflowState,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )
    epic = models.ForeignKey(
        Epic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    current_sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class TaskWorkflowStates(models.Model):
    """
    Audit log of task status changes.
    Records every time a task moves from one workflow state to another.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_workflow_states')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='workflow_history')
    status = models.ForeignKey(WorkflowState, on_delete=models.CASCADE, related_name='task_transitions')
    date_updated = models.DateTimeField(auto_now_add=True)


class TaskCompletionLog(models.Model):
    """
    Records task completion metrics.
    One-to-one relationship with Task to track minutes logged.
    """
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='completion_log'
    )
    minutes_logged = models.IntegerField()
    date_updated = models.DateTimeField(auto_now=True)


class PastSprintMetadata(models.Model):
    """
    Stores aggregated metrics for completed sprints.
    One-to-one relationship with Sprint to track completion statistics.
    """
    sprint = models.OneToOneField(
        Sprint,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='metadata'
    )
    number_of_tasks_completed = models.IntegerField()
    minutes_of_work_completed = models.IntegerField()
    date_completed = models.DateTimeField()
