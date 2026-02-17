### Log

```
February 16, 2026
10:45pm - 12:24am - writing prompts (99min)
```

## Prompts

```
I'm building a productivity app (Django web app with vanilla JavaScript) with the following requirements.

Pages

1) Login (/login): initial page of the application. Users cannot access other pages without logging in first.
2) Home (/): Home page user sees after logging in.
2) Data (/data): Users can edit and save epics, tasks, and workflow states
3) Kanban Board (/board): A Kanban board with the current week's tasks.
4) Calendar (/calendar): A calendar view of how much work was done on each day.
5) Analytics (/analytics): Diagrams, graphs, and charts of my productivity (e.g. a graph)

Note:
- The login page has a stand-alone UI
- The rest of the 5 pages have the following UI
    - Top navbar with
        - A hamburger button on the top left
        - A user button with a dropdown which allows users to logout
    - Hamburger menu slides in from the left when the hamburger button is clicked with the 5 pages listed

Data Schema (SQL Tables)

- users: users of the application
- epics: a grouping of tasks
    - columns: id, user_id, name, display_name, colour, date_created
- workflow_states: the status of a task (e.g. backlog, in progress, done)
    - columns: id, user_id, order (integer), name, display_name, is_on_board, is_final, date_created
        - (user_id, order) form a unique key
- tasks: a unit of work
    - columns: id, user_id, name, display_name, description, current_status_id, epic_id, date_created, current_sprint_id, date_updated
        - note: status_id references id in workflow_states
        - note: epic_id references id in epics (or is null)
        - current_sprint_id references id in sprints (or is null)
- task_workflow_states: log of changes to a task's current_status_id
    - columns: id, user_id, task_id, status_id, date_updated
- task_completion_log: log of task completion events
    - task_id (primary key), minutes_logged, date_updated
- sprint: week-long sprints
    - columns: id, start_date, end_date
- past_sprint_metadata: metadata about a sprint
    - columns: sprint_id, number_of_tasks_completed, minutes_of_work_completed, date_completed
```

```
Please create a plan for creating the database schema.
```

```
Please create a plan for writing the code for the Login page.
```

```
Home page

- Based on the data in past_sprint_metadata, use the number of minutes of work completed for the last 10 weeks to display a chart plotting number of hours of work done over time.

Please create a plan for writing the code for the Home page.
```

```
Please create a plan for implementing a custom-built vanilla javascript implementation of jquery's datatable.
```

```
Data Page

- The content is a tab control with the following tabs: Epics, Tasks, Workflow States

We are writing the content for the Data page. Please create a plan for writing the code for the tab control. It should have no content yet.
```

```
Data Page

- The content is a tab control with the following tabs: Epics, Tasks, Workflow States
- The Epics tab content should use the datatable implementation here: ???????

We are writing the content for the Data page. Please create a plan for writing the code for the Epics tab in the tab control.
```

```
Data Page

- The content is a tab control with the following tabs: Epics, Tasks, Workflow States

We are writing the content for the Data page. Please create a plan for writing the code for the Tasks tab in the tab control. It should follow the same pattern as was done for the Epics tab.
```

```
Data Page

- The content is a tab control with the following tabs: Epics, Tasks, Workflow States

We are writing the content for the Data page. Please create a plan for writing the code for the Workflow States tab in the tab control. It should follow the same pattern as was done for the Epics tab.
```

```
Kanban Board Page

- Content is a grid with each column representing, in order, the workflow states for the user where is_on_board is true
- All tasks for the current sprint are layed out in their appropriate columns (based on the task's current_status_id)

Please create a plan for writing the code for the Kanban Board page.
```

```
Please create a plan for enhancing the code for the Kanban Board page.

- Users can drag and drop tasks into other columns
- When a task is dropped into a workflow state that is final, a modal comes up which asks for the amount of time spent on the task can specify hours (float) or minutes (integer), which gets converted to minutes (integer) to save on the backend.
```

```
Please create a plan for enhancing the code for the Kanban Board page.
- When a task is clicked, but not dragged, on the Kanban Board page, it should bring up a modal with the task name, display name, and description. I should be able to edit the display name and description from this modal with a save button.

```

```
Please create a plan for enhancing the code for the Kanban Board page.
- When a task is clicked, but not dragged, on the Kanban Board page, it should bring up a modal with the task name, display name, and description. I should be able to edit the display name and description from this modal with a save button.

```

```
Calendar Page

- A Monday (first column) to Sunday (last column) view with buttons to switch between months.
- Based on the data in past_sprint_metadata, every week should have a background colour based on the number of hours of work completed in that week
    - [0, 2): red
    - [2, 6): orange
    - [6, 8): yellow
    - [8, 10): green
    - [10, 100]: purple

Please create a plan for writing the code for the Calendar page.
```

```
Please create a plan for enhancing the code for the Calendar page.

- When I click on a particular week, I should see, on a fixed panel on the right hand side, the tasks completed that week.
```



```
Analytics Page

- Based on the data in past_sprint_metadata, use the number of minutes of work completed for the last 10 weeks to display a chart plotting number of hours of work done over time.

Please create a plan for writing the code for the Analytics page.
```


