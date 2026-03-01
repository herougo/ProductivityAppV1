# Database Schema Implementation Plan

## Context

This plan implements the complete database schema for the productivity tracking application. The project is a Django 6.0.2 web app with SQLite database that requires tables for managing tasks, epics, workflow states, sprints, and productivity analytics.

**Current State:**
- Django project exists with default configuration
- No custom Django apps created yet
- Database is empty (no migrations run)
- Only default Django contrib apps are installed

**Goal:**
Create a Django app with models that implement the full schema specified in `ai/documentation/1-plan-overview.md`, including:
- Users (leverage Django's built-in User model)
- Epics (task groupings)
- Workflow States (task statuses with ordering)
- Tasks (core work units)
- Task Workflow State Logs (status change history)
- Task Completion Logs (time tracking)
- Sprints (week-long periods)
- Past Sprint Metadata (sprint statistics)

## Implementation Steps

### 1. Create Django App

**Action:** Create a new Django app named "core" to contain all productivity models.

```bash
cd productivity_app
python manage.py startapp core
```

**Rationale:** Using a single "core" app keeps related models together and avoids circular dependency issues. The schema represents a cohesive productivity tracking domain.

### 2. Register App in Settings

**File:** `productivity_app/productivity_app/settings.py`

**Change:** Add `'core.apps.CoreConfig'` to `INSTALLED_APPS` list (after the default Django apps).

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',  # Add this line
]
```

### 3. Create Django Models

**File:** `productivity_app/core/models.py`

**Models to implement** (in dependency order):

#### 3.1 Epic Model
- Fields: user (FK to User), name, display_name, colour (hex code with validator), date_created
- Ordering: by user and name
- Related name: `user.epics`

#### 3.2 WorkflowState Model
- Fields: user (FK to User), order (PositiveIntegerField), name, display_name, is_on_board, is_final, date_created
- **Unique constraint:** (user, order) - enforces that each user has unique ordering
- Ordering: by user and order
- Related name: `user.workflow_states`

#### 3.3 Sprint Model
- Fields: start_date, end_date
- No user FK (sprints are global/system-wide)
- Ordering: by start_date descending (newest first)
- Property: `is_current` - checks if sprint is currently active

#### 3.4 Task Model
- Fields: user (FK to User), name, display_name, description, current_status (FK to WorkflowState), epic (FK to Epic, nullable), current_sprint (FK to Sprint, nullable), date_created, date_updated
- Foreign key behaviors:
  - current_status: `on_delete=PROTECT` (prevent deletion of in-use workflow states)
  - epic: `on_delete=SET_NULL` (tasks survive epic deletion)
  - current_sprint: `on_delete=SET_NULL` (tasks survive sprint deletion)
- Ordering: by user and date_updated descending
- Related names: `user.tasks`, `epic.tasks`, `sprint.tasks`, `workflow_state.tasks`
- Method: `change_status(new_status)` - updates status and creates log entry

#### 3.5 TaskWorkflowStateLog Model
- Fields: user (FK to User), task (FK to Task), status (FK to WorkflowState), date_updated (auto)
- Purpose: Historical log of all task status changes
- Ordering: by task and date_updated descending
- Related names: `task.status_logs`, `user.task_status_logs`

#### 3.6 TaskCompletionLog Model
- Fields: task (OneToOneField as primary key), minutes_logged, date_updated (auto)
- Purpose: Track time spent on completed tasks
- One completion log per task
- Related name: `task.completion_log`

#### 3.7 PastSprintMetadata Model
- Fields: sprint (OneToOneField as primary key), number_of_tasks_completed, minutes_of_work_completed, date_completed
- Purpose: Store aggregate statistics for completed sprints
- One metadata record per sprint
- Related name: `sprint.metadata`

**Key Design Decisions:**
- Use `settings.AUTH_USER_MODEL` for user references (future-proof)
- Use `auto_now_add=True` for date_created fields
- Use `auto_now=True` for date_updated fields
- Add database indexes for common query patterns (user filters, date sorting, FK lookups)
- Use appropriate `on_delete` behaviors to maintain data integrity
- Include helpful `help_text` for fields
- Add regex validator for colour field (hex codes only)

### 4. Configure Django Admin

**File:** `productivity_app/core/admin.py`

**Action:** Register all models with Django admin interface for easy data management during development.

**Admin classes to create:**
- `EpicAdmin` - display name, user, colour, date_created; filterable by user
- `WorkflowStateAdmin` - display name, user, order, flags; filterable by user and flags
- `SprintAdmin` - id, dates, is_current property
- `TaskAdmin` - display name, user, status, epic, sprint, date_updated; filterable by all FKs
- `TaskWorkflowStateLogAdmin` - task, status, user, date; read-only historical data
- `TaskCompletionLogAdmin` - task, minutes, date
- `PastSprintMetadataAdmin` - sprint, stats, date

**Features:**
- Use `list_display` for key fields
- Use `list_filter` for common filters (user, dates, statuses)
- Use `search_fields` for text search (names, display_names)
- Use `raw_id_fields` for ForeignKeys to avoid dropdown performance issues with many records
- Use `ordering` for consistent display

### 5. Create and Apply Migrations

**Actions:**

```bash
# Generate initial migration for core app
python manage.py makemigrations core

# Apply all migrations (including default Django migrations)
python manage.py migrate
```

**Expected outcome:**
- Creates `core/migrations/0001_initial.py` with all model definitions
- Creates database tables for all models
- Django handles circular ForeignKey references automatically

### 6. Create Superuser

**Action:** Create admin user for accessing Django admin interface.

```bash
python manage.py createsuperuser
```

**Purpose:** Allows testing models via admin interface at `http://localhost:8000/admin/`

### 7. (Optional) Create Management Command for Default Workflow States

**File:** `productivity_app/core/management/commands/create_default_workflow.py`

**Purpose:** Provide a management command to initialize default workflow states for new users.

**Default states:**
1. Backlog (order=1, not on board, not final)
2. To Do (order=2, on board, not final)
3. In Progress (order=3, on board, not final)
4. Review (order=4, on board, not final)
5. Done (order=5, on board, final)

**Usage:** `python manage.py create_default_workflow <username>`

**Note:** This can be called after user registration or handled via Django signals.

## Critical Files

- `productivity_app/core/models.py` - All model definitions
- `productivity_app/core/admin.py` - Django admin configuration
- `productivity_app/productivity_app/settings.py` - Register core app
- `productivity_app/core/migrations/0001_initial.py` - Generated migration file
- `productivity_app/core/management/commands/create_default_workflow.py` - Optional utility command

## Verification Steps

After implementation, verify the database schema is correctly created:

### 1. Check Migration Files
```bash
cd productivity_app
python manage.py showmigrations core
```

Expected output: `[X] 0001_initial`

### 2. Verify Database Schema
```bash
# Using SQLite CLI (if installed)
sqlite3 db.sqlite3 ".schema"

# Or using Django dbshell
python manage.py dbshell
.tables
.schema core_epic
.schema core_task
.quit
```

Expected tables:
- `core_epic`
- `core_workflowstate`
- `core_sprint`
- `core_task`
- `core_taskworkflowstatelog`
- `core_taskcompletionlog`
- `core_pastsprintmetadata`

### 3. Test Django Admin Interface
```bash
python manage.py runserver
```

Visit `http://localhost:8000/admin/` and verify:
- All 7 models appear in admin
- Can create/edit/delete records
- List views show correct columns
- Filters work correctly

### 4. Test Model Relationships
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from core.models import Epic, WorkflowState, Task

User = get_user_model()

# Create test user
user = User.objects.create_user(username='testuser', password='test123')

# Create epic
epic = Epic.objects.create(
    user=user,
    name='test_epic',
    display_name='Test Epic',
    colour='#FF5733'
)

# Create workflow state
state = WorkflowState.objects.create(
    user=user,
    order=1,
    name='backlog',
    display_name='Backlog',
    is_on_board=False,
    is_final=False
)

# Create task
task = Task.objects.create(
    user=user,
    name='test_task',
    display_name='Test Task',
    description='A test task',
    current_status=state,
    epic=epic
)

# Verify relationships
print(f"Epic tasks: {epic.tasks.count()}")  # Should be 1
print(f"State tasks: {state.tasks.count()}")  # Should be 1
print(f"User tasks: {user.tasks.count()}")  # Should be 1
```

### 5. Test Unique Constraint
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from core.models import WorkflowState
from django.db import IntegrityError

User = get_user_model()
user = User.objects.first()

# Create first state with order=1
WorkflowState.objects.create(
    user=user, order=1, name='state1', display_name='State 1'
)

# Try to create second state with same order=1 (should fail)
try:
    WorkflowState.objects.create(
        user=user, order=1, name='state2', display_name='State 2'
    )
    print("ERROR: Unique constraint not enforced!")
except IntegrityError:
    print("SUCCESS: Unique constraint working correctly")
```

## Dependencies

- Django 6.0.2 (already in requirements.txt)
- Python 3.14 (current environment)
- SQLite (built into Python, no additional install needed)

## Notes

- **Timezone:** Project currently uses `TIME_ZONE = 'UTC'` in settings.py. If user prefers different timezone, update settings before creating migrations.
- **User Authentication:** This plan uses Django's built-in User model. If additional user fields are needed later (profile picture, bio, etc.), create a separate `UserProfile` model with OneToOne relationship.
- **Sprint Auto-Creation:** Consider implementing a management command or scheduled task to automatically create weekly sprints.
- **Signals:** Could add Django signals to automatically create TaskWorkflowStateLog entries when Task.current_status changes (instead of manual `change_status()` method).
- **Performance:** Indexes are included for common query patterns. For production with large data volumes, consider additional indexes based on actual query patterns.

## Future Enhancements (Out of Scope)

- Add Django signals for automatic log creation
- Add model managers for common queries (e.g., `Task.objects.completed()`)
- Add data validation (e.g., sprint end_date must be after start_date)
- Add cascade protection for workflow states with completed tasks
- Create fixtures for test data
- Add comprehensive unit tests for models
