# Task 05: Register Models in Admin

## Overview

Register all productivity_core models with Django admin to enable data management through the admin interface.

## Files to Modify

### `productivity_app/productivity_core/admin.py`

**Current state:**
- Empty file with only default Django import and comment

**Changes needed:**
1. Import all models from models.py
2. Register each model with admin.site.register()

**Implementation details:**

Add the following imports:
```python
from .models import (
    Epic,
    WorkflowState,
    Task,
    TaskWorkflowStates,
    TaskCompletionLog,
    Sprint,
    PastSprintMetadata
)
```

Register each model:
```python
admin.site.register(Epic)
admin.site.register(WorkflowState)
admin.site.register(Task)
admin.site.register(TaskWorkflowStates)
admin.site.register(TaskCompletionLog)
admin.site.register(Sprint)
admin.site.register(PastSprintMetadata)
```

## Expected Outcome

After completing this task:
- All 7 models will be visible in the Django admin interface
- Admin users can view, create, edit, and delete records for each model
- The models will display using their default representation (can be enhanced later with custom ModelAdmin classes)

## Notes

- This is a basic registration - custom ModelAdmin classes can be added later for better UX
- The admin interface will be accessible at `/admin/` (if admin URLs are configured)
- Default display will show model names and basic field information
