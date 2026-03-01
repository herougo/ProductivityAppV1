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
