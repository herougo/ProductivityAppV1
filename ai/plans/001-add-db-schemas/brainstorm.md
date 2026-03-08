# Brainstorm: Database Schema Implementation

## Context
Creating the database schema for a Django-based productivity tracking application with the following entities:
- Users
- Epics (task groupings)
- Workflow States (task statuses)
- Tasks (units of work)
- Task Workflow States (status change log)
- Task Completion Log
- Sprints (week-long periods)
- Past Sprint Metadata

## Clarifying Questions

### 1. User Model
- **Question:** Should we use Django's built-in `User` model, extend it with `AbstractUser`, or use `AbstractBaseUser` for a completely custom implementation?
- **Consideration:** The schema shows a simple "users" table. Django's built-in User provides username, email, password, and more out of the box.

### 2. Data Integrity & Constraints
- **Question:** Should we enforce additional constraints beyond those mentioned?
  - Unique constraint on `epics.name` per user?
  - Unique constraint on `workflow_states.name` per user?
  - Unique constraint on `tasks.name` per user?
  - Check constraint to ensure sprint `start_date < end_date`?

### 3. Deletion Behavior
- **Question:** What should happen when referenced records are deleted?
  - If an Epic is deleted, should tasks be set to NULL or cascade delete?
  - If a Workflow State is deleted, what happens to tasks using it?
  - Should we use soft deletes (is_deleted flag) instead of hard deletes?

### 4. Indexes
- **Question:** Should we add database indexes for performance?
  - Index on `tasks.user_id, tasks.current_sprint_id` for board queries?
  - Index on `task_workflow_states.task_id, task_workflow_states.date_updated` for history queries?

### 5. Default Workflow States
- **Question:** Should we create default workflow states (Backlog, In Progress, Done) for new users automatically?

### 6. Sprint Management
- **Question:** How are sprints created?
  - Automatically generated based on calendar weeks?
  - Manually created by users?
  - One sprint table for all users or per-user sprints?

## Approach 1: Single-App Monolithic

### Structure
- Create one Django app: `productivity_core`
- All models in `productivity_core/models.py`
- Single migration creates all tables at once

### Pros
- Simple structure, easy to understand
- All related models in one place
- Easier to manage foreign key relationships
- Less complexity in Django app configuration

### Cons
- Models file could become large
- Less modular for future scaling
- Harder to reuse components in other projects

### Implementation Steps
1. Create `productivity_core` app
2. Define all models in `models.py`
3. Register models in admin
4. Create and run migrations
5. Add model methods and properties

---

## Approach 2: Multi-App Domain-Driven

### Structure
Split into domain-focused apps:
- `users` - User model and profile
- `workflow` - Epic, WorkflowState models
- `tasks` - Task, TaskWorkflowStates, TaskCompletionLog models
- `sprints` - Sprint, PastSprintMetadata models

### Pros
- Clean separation of concerns
- Each app is independently testable
- Can reuse apps in other projects
- Follows Django best practices for larger projects
- Easier to assign ownership in team settings

### Cons
- More complex project structure
- Cross-app foreign keys require careful management
- More migration files to manage
- Overkill for a smaller project

### Implementation Steps
1. Create each Django app
2. Define models in respective apps
3. Configure app dependencies
4. Handle cross-app foreign keys with string references
5. Create migrations for each app
6. Register admin interfaces per app

---

## Approach 3: Incremental Core-First

### Structure
- Start with `core` app containing User, Epic, WorkflowState
- Add `tasks` app with Task model
- Add `tracking` app with logging tables
- Add `sprints` app last

### Pros
- Allows testing core functionality first
- Can validate schema design incrementally
- Easier to catch issues early
- Natural migration path for development
- Can deploy features incrementally

### Cons
- Requires more planning of dependencies
- Multiple rounds of testing
- Some rework might be needed between phases
- Takes longer to have full feature set

### Implementation Steps (Phased)

**Phase 1: Foundation**
1. Create `core` app
2. Add User (or use Django's built-in)
3. Add Epic model
4. Add WorkflowState model
5. Test and validate

**Phase 2: Task Management**
1. Create `tasks` app
2. Add Task model with FK to Epic and WorkflowState
3. Add basic task CRUD functionality
4. Test task creation and status changes

**Phase 3: Tracking & History**
1. Add TaskWorkflowStates model for history
2. Add TaskCompletionLog model
3. Add signals to auto-log changes
4. Test logging functionality

**Phase 4: Sprint Management**
1. Create `sprints` app
2. Add Sprint model
3. Add PastSprintMetadata model
4. Add sprint-task relationships
5. Test sprint functionality

---

## Recommendation

**For this project, I recommend Approach 1 (Single-App Monolithic)** because:

1. **Project Size:** This is a learning project focused on Django fundamentals - complexity should be minimized
2. **Cohesion:** All models are tightly related to productivity tracking
3. **Simplicity:** Easier to understand and maintain for a single developer
4. **Iteration Speed:** Faster to implement and test the complete system
5. **Schema Clarity:** The entire data model is visible in one place

However, we should structure the models file with clear sections and comprehensive docstrings to maintain readability as it grows.

## Additional Implementation Considerations

### 1. Model Enhancements
- Add `__str__()` methods for readable admin interface
- Add `Meta` classes with `ordering` for consistent query results
- Add model methods for common operations (e.g., `task.complete()`, `task.move_to_status()`)

### 2. Data Validation
- Add validators for color fields in Epic
- Ensure workflow state order values are positive integers
- Validate sprint date ranges

### 3. Signals
- Use Django signals to automatically create TaskWorkflowStates entries when task status changes
- Auto-update `date_updated` fields on save

### 4. Admin Interface
- Create custom admin classes for better UX
- Add inline editing for related models
- Add filters and search capabilities

### 5. Initial Data
- Create management command to set up default workflow states
- Optionally create sample epics for new users
