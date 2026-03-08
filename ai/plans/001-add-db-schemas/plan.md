# Database Schema Implementation Plan

## Notes

This plan implements the complete database schema for the productivity tracking application using **Approach 1 (Single-App Monolithic)** as recommended in the brainstorm. All models will be created in a single Django app called `productivity_core`.

**Key Decisions:**
- Use Django's built-in User model
- Epic deletion sets task `epic_id` to NULL
- Workflow State deletion sets task `current_status_id` to "Backlog" (or NULL); "Backlog" state cannot be deleted
- Default workflow states (Backlog, In Progress, Done) created automatically for new users
- No additional unique constraints or indexes initially (can be added later)
- No soft deletes

**Database Tables:**
- users (Django built-in)
- epics
- workflow_states
- tasks
- task_workflow_states
- task_completion_log
- sprints
- past_sprint_metadata

## Task Overview

- [x] 01 - **Create productivity_core app** - Create the Django app that will contain all models
- [ ] 02 - **Configure Django app** - Add productivity_core to INSTALLED_APPS in settings.py
- [ ] 03 - **Define all models** - Create all database models in models.py
- [ ] 04 - **Create and run migrations** - Generate and apply database migrations
- [ ] 05 - **Register models in admin** - Configure Django admin interface for all models
- [ ] 06 - **Add model enhancements** - Add __str__ methods, Meta classes, and helper methods
- [ ] 07 - **Create default workflow states setup** - Add management command to create default workflow states

## Task Details

### 01 - Create productivity_core app

**Type:** User command

**Description:** Create the Django app that will house all productivity-related models.

**Commands to run:**
```bash
cd productivity_app
python manage.py startapp productivity_core
```

**Notes:** Run from the `productivity_app/` directory (where manage.py is located).

---

### 02 - Configure Django app

**Type:** Code changes

**Description:** Register the new productivity_core app in Django settings.

**Files to modify:**
- `productivity_app/productivity_app/settings.py`
  - Add `'productivity_core',` to the `INSTALLED_APPS` list

**Notes:** Add it after the default Django apps but before any third-party apps (if applicable).

---

### 03 - Define all models

**Type:** Code changes

**Description:** Create all database models according to the schema specification.

**Files to modify:**
- `productivity_app/productivity_core/models.py`

**Models to create:**
1. **Epic**
   - Fields: user (FK), name, display_name, colour, date_created
   - Foreign keys: user → User (CASCADE)

2. **WorkflowState**
   - Fields: user (FK), order, name, display_name, is_on_board, is_final, date_created
   - Foreign keys: user → User (CASCADE)
   - Unique constraint: (user, order)
   - Add custom delete protection for "Backlog" state

3. **Task**
   - Fields: user (FK), name, display_name, description, current_status (FK), epic (FK), date_created, current_sprint (FK), date_updated
   - Foreign keys:
     - user → User (CASCADE)
     - current_status → WorkflowState (SET to Backlog or NULL)
     - epic → Epic (SET_NULL)
     - current_sprint → Sprint (SET_NULL)

4. **TaskWorkflowStates**
   - Fields: user (FK), task (FK), status (FK), date_updated
   - Foreign keys: user → User (CASCADE), task → Task (CASCADE), status → WorkflowState (CASCADE)

5. **TaskCompletionLog**
   - Fields: task (FK, PRIMARY KEY), minutes_logged, date_updated
   - Foreign keys: task → Task (CASCADE)

6. **Sprint**
   - Fields: user (FK), start_date, end_date
   - Foreign keys: user → User (CASCADE)
   - Add validation: start_date < end_date

7. **PastSprintMetadata**
   - Fields: sprint (FK, PRIMARY KEY), number_of_tasks_completed, minutes_of_work_completed, date_completed
   - Foreign keys: sprint → Sprint (CASCADE)

**Notes:**
- Import User model: `from django.contrib.auth.models import User`
- Use appropriate field types (CharField, TextField, ForeignKey, DateTimeField, IntegerField, etc.)
- Set `auto_now_add=True` for date_created fields
- Set `auto_now=True` for date_updated fields where applicable
- Add docstrings to each model explaining its purpose

---

### 04 - Create and run migrations

**Type:** User command

**Description:** Generate migration files and apply them to create database tables.

**Commands to run:**
```bash
cd productivity_app
python manage.py makemigrations
python manage.py migrate
```

**Expected output:**
- Migration file created in `productivity_core/migrations/0001_initial.py`
- Database tables created successfully

---

### 05 - Register models in admin

**Type:** Code changes

**Description:** Register all models with Django admin for easy data management.

**Files to modify:**
- `productivity_app/productivity_core/admin.py`

**Models to register:**
- Epic
- WorkflowState
- Task
- TaskWorkflowStates
- TaskCompletionLog
- Sprint
- PastSprintMetadata

**Notes:**
- Use `admin.site.register()` for each model
- Can enhance later with custom ModelAdmin classes for better UX

---

### 06 - Add model enhancements

**Type:** Code changes

**Description:** Add __str__ methods, Meta classes, and helper methods to improve model usability.

**Files to modify:**
- `productivity_app/productivity_core/models.py`

**Enhancements to add:**

1. **__str__ methods** for all models (for readable admin interface)
   - Epic: return display_name or name
   - WorkflowState: return display_name or name
   - Task: return display_name or name
   - etc.

2. **Meta classes**
   - Add `ordering` for consistent query results
   - Add `verbose_name` and `verbose_name_plural` where appropriate
   - Add `db_table` if needed for explicit table naming

3. **Helper methods** (examples)
   - `Task.complete()` - mark task as complete
   - `Task.move_to_status(status)` - change task status
   - `Sprint.is_current()` - check if sprint is currently active

**Notes:**
- Keep methods simple and focused
- Add docstrings for complex methods

---

### 07 - Create default workflow states setup

**Type:** Code changes

**Description:** Create a management command to set up default workflow states for new users.

**Files to create:**
- `productivity_app/productivity_core/management/__init__.py` (empty file)
- `productivity_app/productivity_core/management/commands/__init__.py` (empty file)
- `productivity_app/productivity_core/management/commands/create_default_workflow_states.py`

**Command functionality:**
- Create default workflow states: Backlog (order=1, is_on_board=False), In Progress (order=2, is_on_board=True), Done (order=3, is_on_board=True, is_final=True)
- Accept user_id as argument or create for all users without workflow states
- Skip users who already have workflow states

**Notes:**
- This command can be run manually or integrated into user creation flow later
- Consider adding this to a post_save signal for User model in the future
