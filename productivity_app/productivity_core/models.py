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

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Epic'
        verbose_name_plural = 'Epics'

    def __str__(self):
        return self.display_name


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
        ordering = ['order']
        verbose_name = 'Workflow State'
        verbose_name_plural = 'Workflow States'
        constraints = [
            models.UniqueConstraint(fields=['user', 'order'], name='unique_user_order')
        ]

    def __str__(self):
        return f"{self.display_name} (order: {self.order})"


class Sprint(models.Model):
    """
    Represents week-long sprints for organizing work.
    Each sprint has a start and end date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sprints')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'

    def __str__(self):
        return f"Sprint {self.start_date} to {self.end_date}"

    def is_current(self):
        """
        Check if this sprint is currently active (today's date falls within the sprint).

        Returns:
            bool: True if sprint is active, False otherwise
        """
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


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

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.display_name

    def move_to_status(self, status):
        """
        Move task to a new workflow state and create audit log entry.

        Args:
            status: WorkflowState instance to move the task to
        """
        from django.utils import timezone

        # Update current status
        self.current_status = status
        self.save()

        # Create audit log entry
        TaskWorkflowStates.objects.create(
            user=self.user,
            task=self,
            status=status,
            date_updated=timezone.now()
        )

    def complete(self, minutes_logged=0):
        """
        Mark task as complete by moving it to a final workflow state.
        Creates or updates completion log entry.

        Args:
            minutes_logged: Number of minutes spent on the task (default: 0)

        Returns:
            bool: True if task was completed, False if no final state exists
        """
        # Find a final workflow state for this user
        final_state = WorkflowState.objects.filter(
            user=self.user,
            is_final=True
        ).first()

        if not final_state:
            return False

        # Move to final state
        self.move_to_status(final_state)

        # Create or update completion log
        TaskCompletionLog.objects.update_or_create(
            task=self,
            defaults={'minutes_logged': minutes_logged}
        )

        return True


class TaskWorkflowStates(models.Model):
    """
    Audit log of task status changes.
    Records every time a task moves from one workflow state to another.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_workflow_states')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='workflow_history')
    status = models.ForeignKey(WorkflowState, on_delete=models.CASCADE, related_name='task_transitions')
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'Task Workflow State'
        verbose_name_plural = 'Task Workflow States'

    def __str__(self):
        return f"{self.task.display_name} → {self.status.display_name} ({self.date_updated.strftime('%Y-%m-%d %H:%M')})"


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

    class Meta:
        verbose_name = 'Task Completion Log'
        verbose_name_plural = 'Task Completion Logs'

    def __str__(self):
        return f"{self.task.display_name}: {self.minutes_logged} minutes"


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

    class Meta:
        verbose_name = 'Past Sprint Metadata'
        verbose_name_plural = 'Past Sprint Metadata'

    def __str__(self):
        return f"Sprint {self.sprint}: {self.number_of_tasks_completed} tasks, {self.minutes_of_work_completed} minutes"
