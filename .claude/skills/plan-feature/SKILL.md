---
name: plan-feature
description: Plan a feature.
---

Please do the following.

1) Read @ai/documentation/1-plan-overview.md for context.
2) Read @ai/plans/$0/1-human-prompt.md for context on the feature you will eventually implement.
3) If it exists, read @ai/plans/$0/brainstorm.md for context on ideas from the brainstorming session.
4) Create a plan for the feature outlined in @ai/plans/$0/1-human-prompt.md . Please do the following.
    - Break the feature into tasks where each task is either
        a) A command that the user must run themselves (e.g. Django command)
        b) Edits to the code base (simple file and folder creation/edits/deletion only).
    - Each task is expected to be a single commit, so it should small enough in scope to be easy to review.
    - Do NOT change any files at this time.
5) Write your plan to @ai/plans/$0/plan.md. Use the following format for the plan.

### plan.md Format

```
# (Plan Title)

## Notes

(Context or constraints)

## Task Overview

- [ ] 01 - **(Task name)** - (Task description)
- [ ] 02 - **(Task name)** - (Task description)
...

## Task Details

### 01 - (Task Name)
...

### 02 - (Task Name)
...

```