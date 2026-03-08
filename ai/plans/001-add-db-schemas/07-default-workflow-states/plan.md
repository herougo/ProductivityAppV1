# Task Plan: Create Default Workflow States Setup

## Overview

Create a Django management command that sets up default workflow states for users. This allows administrators to easily create the standard "Backlog", "In Progress", and "Done" workflow states for new users or users without existing workflow states.

## Files to Create

1. `productivity_app/productivity_core/management/__init__.py` - Empty init file
2. `productivity_app/productivity_core/management/commands/__init__.py` - Empty init file
3. `productivity_app/productivity_core/management/commands/create_default_workflow_states.py` - Management command implementation

## Implementation Details

### 1. Create Directory Structure

Create the following directory structure:
```
productivity_app/productivity_core/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── create_default_workflow_states.py
```

### 2. Management Command Implementation

**File:** `productivity_app/productivity_core/management/commands/create_default_workflow_states.py`

**Command Name:** `create_default_workflow_states`

**Usage Examples:**
```bash
# Create default workflow states for all users without them
python manage.py create_default_workflow_states

# Create default workflow states for a specific user
python manage.py create_default_workflow_states --user-id 1

# Create default workflow states for multiple users
python manage.py create_default_workflow_states --user-id 1 --user-id 2
```

**Implementation Requirements:**

1. **Command Structure:**
   - Inherit from `BaseCommand`
   - Define help text explaining the command's purpose
   - Add command-line arguments for optional user filtering

2. **Command Arguments:**
   - `--user-id` (optional, can be specified multiple times): Target specific user IDs
   - If no user IDs provided: process all users who don't have workflow states

3. **Default Workflow States to Create:**
   - **Backlog**
     - order: 1
     - name: "backlog"
     - display_name: "Backlog"
     - is_on_board: False
     - is_final: False

   - **In Progress**
     - order: 2
     - name: "in_progress"
     - display_name: "In Progress"
     - is_on_board: True
     - is_final: False

   - **Done**
     - order: 3
     - name: "done"
     - display_name: "Done"
     - is_on_board: True
     - is_final: True

4. **Logic Flow:**
   ```
   1. Determine target users (specific IDs or all users without workflow states)
   2. For each target user:
      a. Check if user already has workflow states
      b. If yes: skip with message
      c. If no: create the 3 default workflow states
      d. Output success message
   3. Provide summary of how many users were processed
   ```

5. **Error Handling:**
   - Handle invalid user IDs gracefully
   - Handle database errors with informative messages
   - Use Django's `self.stdout.write()` for success messages (green)
   - Use `self.stderr.write()` for warnings/errors (yellow/red)

6. **Output Messages:**
   - Success: "✓ Created default workflow states for user {user_id} ({username})"
   - Skip: "- User {user_id} ({username}) already has workflow states"
   - Error: "✗ Error processing user {user_id}: {error}"
   - Summary: "Processed {total} users: {created} created, {skipped} skipped"

### 3. Code Template Structure

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from productivity_core.models import WorkflowState


class Command(BaseCommand):
    help = 'Create default workflow states (Backlog, In Progress, Done) for users'

    def add_arguments(self, parser):
        # Add --user-id argument (optional, multiple values allowed)
        pass

    def handle(self, *args, **options):
        # Get target users
        # For each user:
        #   - Check if has workflow states
        #   - If not, create default states
        #   - Output appropriate message
        # Print summary
        pass

    def create_default_workflow_states(self, user):
        """Create the three default workflow states for a user."""
        # Create Backlog, In Progress, Done
        pass

    def user_has_workflow_states(self, user):
        """Check if user already has any workflow states."""
        # Return True/False
        pass
```

### 4. Implementation Notes

**Best Practices:**
- Use `self.style.SUCCESS()` for green success messages
- Use `self.style.WARNING()` for yellow warning messages
- Use `self.style.ERROR()` for red error messages
- Use transactions for atomic operations (all 3 states created or none)
- Include verbose output showing progress

**Safety:**
- Never overwrite existing workflow states
- Always check before creating
- Validate user existence before attempting creation

**Database Operations:**
- Use `bulk_create()` for efficiency when creating multiple states
- Use `exists()` to check for existing states (more efficient than `count()`)
- Wrap state creation in `transaction.atomic()` for data consistency

**Testing Suggestions:**
After implementation, test with:
```bash
# Test with non-existent user
python manage.py create_default_workflow_states --user-id 999

# Test with existing user
python manage.py create_default_workflow_states --user-id 1

# Test running twice on same user (should skip)
python manage.py create_default_workflow_states --user-id 1

# Test with all users
python manage.py create_default_workflow_states
```

## Future Enhancements (Not Part of This Task)

These are noted for future consideration but NOT implemented in this task:
- Add to User model's `post_save` signal for automatic creation
- Make default states configurable via settings
- Add ability to customize state names/colors via command arguments
- Add `--force` flag to recreate states if they exist

## Expected Outcome

After completing this task:
1. Administrators can run the management command to set up workflow states
2. New users can be quickly onboarded with standard workflow states
3. The command provides clear feedback about what was created
4. The command is safe to run multiple times (idempotent)
