# Task Plan: Add Model Enhancements

## Overview

This task enhances the Django models in `productivity_core` by adding:
1. `__str__` methods for readable object representations in admin and shell
2. `Meta` classes for ordering, verbose names, and other metadata
3. Helper methods for common operations

## File to Modify

- `productivity_app/productivity_core/models.py`

## Implementation Details

### 1. Add __str__ Methods

Add `__str__` methods to all models for better readability in Django admin and shell:

**Epic:**
```python
def __str__(self):
    return self.display_name
```

**WorkflowState:**
```python
def __str__(self):
    return f"{self.display_name} (order: {self.order})"
```

**Sprint:**
```python
def __str__(self):
    return f"Sprint {self.start_date} to {self.end_date}"
```

**Task:**
```python
def __str__(self):
    return self.display_name
```

**TaskWorkflowStates:**
```python
def __str__(self):
    return f"{self.task.display_name} → {self.status.display_name} ({self.date_updated.strftime('%Y-%m-%d %H:%M')})"
```

**TaskCompletionLog:**
```python
def __str__(self):
    return f"{self.task.display_name}: {self.minutes_logged} minutes"
```

**PastSprintMetadata:**
```python
def __str__(self):
    return f"Sprint {self.sprint}: {self.number_of_tasks_completed} tasks, {self.minutes_of_work_completed} minutes"
```

### 2. Add/Enhance Meta Classes

Add or enhance `Meta` classes for each model:

**Epic:**
```python
class Meta:
    ordering = ['-date_created']
    verbose_name = 'Epic'
    verbose_name_plural = 'Epics'
```

**WorkflowState:**
```python
class Meta:
    ordering = ['order']
    verbose_name = 'Workflow State'
    verbose_name_plural = 'Workflow States'
    constraints = [
        models.UniqueConstraint(fields=['user', 'order'], name='unique_user_order')
    ]
```
*Note: This model already has a Meta class with constraints - extend it rather than replace it.*

**Sprint:**
```python
class Meta:
    ordering = ['-start_date']
    verbose_name = 'Sprint'
    verbose_name_plural = 'Sprints'
```

**Task:**
```python
class Meta:
    ordering = ['-date_updated']
    verbose_name = 'Task'
    verbose_name_plural = 'Tasks'
```

**TaskWorkflowStates:**
```python
class Meta:
    ordering = ['-date_updated']
    verbose_name = 'Task Workflow State'
    verbose_name_plural = 'Task Workflow States'
```

**TaskCompletionLog:**
```python
class Meta:
    verbose_name = 'Task Completion Log'
    verbose_name_plural = 'Task Completion Logs'
```

**PastSprintMetadata:**
```python
class Meta:
    verbose_name = 'Past Sprint Metadata'
    verbose_name_plural = 'Past Sprint Metadata'
```

### 3. Add Helper Methods

Add useful helper methods to relevant models:

**Task model - Add these methods:**

1. `move_to_status(status)` - Move task to a new workflow state
```python
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
```

2. `complete(minutes_logged=0)` - Mark task as complete
```python
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
```

**Sprint model - Add this method:**

1. `is_current()` - Check if sprint is currently active
```python
def is_current(self):
    """
    Check if this sprint is currently active (today's date falls within the sprint).

    Returns:
        bool: True if sprint is active, False otherwise
    """
    from django.utils import timezone
    today = timezone.now().date()
    return self.start_date <= today <= self.end_date
```

## Implementation Notes

- Keep all methods simple and focused on single responsibilities
- Add docstrings to all helper methods explaining parameters and return values
- Use Django's `timezone.now()` instead of Python's `datetime.now()` for timezone awareness
- The `move_to_status()` method automatically creates audit log entries
- The `complete()` method combines status update with completion logging
- WorkflowState already has a Meta class - ensure we extend it rather than replace it

## Testing Recommendations

After implementing these enhancements, test in Django shell:
```python
# Test __str__ methods
python manage.py shell
>>> from productivity_core.models import Epic, Task, WorkflowState
>>> epic = Epic.objects.first()
>>> print(epic)  # Should show display_name

# Test helper methods
>>> task = Task.objects.first()
>>> task.complete(minutes_logged=120)
>>> task.is_current()

# Test ordering
>>> Task.objects.all()  # Should be ordered by -date_updated
```
