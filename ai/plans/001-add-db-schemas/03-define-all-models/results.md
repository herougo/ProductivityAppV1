# Task Results: Define All Models

## Summary

Successfully defined all 7 database models in `productivity_app/productivity_core/models.py`. All models follow the schema specification and are properly ordered to avoid forward reference issues.

## Changes Made

### File Modified: `productivity_app/productivity_core/models.py`

Replaced the default empty file with complete model definitions including:

1. **Epic Model**
   - Fields: user (FK), name, display_name, colour, date_created
   - Foreign key to User with CASCADE delete
   - Related name: 'epics'

2. **WorkflowState Model**
   - Fields: user (FK), order, name, display_name, is_on_board, is_final, date_created
   - Foreign key to User with CASCADE delete
   - **UniqueConstraint** on (user, order) named 'unique_user_order'
   - Related name: 'workflow_states'

3. **Sprint Model**
   - Fields: user (FK), start_date, end_date
   - Foreign key to User with CASCADE delete
   - Related name: 'sprints'

4. **Task Model**
   - Fields: user (FK), name, display_name, description, current_status (FK), epic (FK), current_sprint (FK), date_created, date_updated
   - Foreign keys configured:
     - user → User (CASCADE)
     - current_status → WorkflowState (SET_NULL, null=True)
     - epic → Epic (SET_NULL, null=True, blank=True)
     - current_sprint → Sprint (SET_NULL, null=True, blank=True)
   - Related name: 'tasks'
   - Auto-updates date_updated on save

5. **TaskWorkflowStates Model**
   - Fields: user (FK), task (FK), status (FK), date_updated
   - All foreign keys use CASCADE delete
   - Related names: 'task_workflow_states', 'workflow_history', 'task_transitions'

6. **TaskCompletionLog Model**
   - Fields: task (OneToOneField, PRIMARY KEY), minutes_logged, date_updated
   - OneToOne relationship with Task as primary key
   - CASCADE delete behavior
   - Related name: 'completion_log'

7. **PastSprintMetadata Model**
   - Fields: sprint (OneToOneField, PRIMARY KEY), number_of_tasks_completed, minutes_of_work_completed, date_completed
   - OneToOne relationship with Sprint as primary key
   - CASCADE delete behavior
   - Related name: 'metadata'

## Implementation Details

### Imports
- Added `from django.contrib.auth.models import User`

### Field Types Used
- `CharField` with appropriate max_length for names and display names
- `CharField(max_length=7)` for hex color codes
- `TextField` for task descriptions
- `IntegerField` for order, counters, and minutes
- `BooleanField` for flags
- `DateTimeField` with auto_now_add=True for date_created
- `DateTimeField` with auto_now=True for date_updated
- `DateField` for sprint dates
- `ForeignKey` and `OneToOneField` for relationships

### Model Ordering
Models are ordered to avoid forward references:
1. Epic (depends only on User)
2. WorkflowState (depends only on User)
3. Sprint (depends only on User)
4. Task (depends on User, WorkflowState, Epic, Sprint)
5. TaskWorkflowStates (depends on User, Task, WorkflowState)
6. TaskCompletionLog (depends on Task)
7. PastSprintMetadata (depends on Sprint)

### Docstrings
Each model includes a docstring explaining its purpose.

### Related Names
All foreign keys include meaningful related_name attributes for reverse lookups:
- User → epics, workflow_states, sprints, tasks, task_workflow_states
- WorkflowState → tasks, task_transitions
- Epic → tasks
- Sprint → tasks, metadata
- Task → workflow_history, completion_log

## Success Criteria Checklist

- [x] All 7 models are defined in models.py
- [x] All fields match the schema specification
- [x] Foreign key relationships are correctly configured with appropriate on_delete behavior
- [x] UniqueConstraint is added to WorkflowState for (user, order)
- [x] auto_now_add and auto_now are used appropriately for timestamp fields
- [x] Models are ordered to avoid forward reference issues
- [x] File has proper imports (User model from django.contrib.auth.models)
- [x] Each model has a docstring explaining its purpose

## Next Steps

The next task (04 - Create and run migrations) will:
1. Generate migration files with `python manage.py makemigrations`
2. Apply migrations with `python manage.py migrate`
3. Create the database tables for all these models
