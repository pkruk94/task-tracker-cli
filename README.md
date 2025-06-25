# Task Tracker CLI

https://roadmap.sh/projects/task-tracker

A simple command-line application for managing your to-do list, written in Python.  
You can add, update, delete, and change the status of your tasks. All tasks are stored in the `tasks.json` file.

## Features

- Add new tasks
- Update task descriptions
- Delete tasks
- Mark tasks as "in progress" or "done"
- List all tasks or filter by status

## Usage

From your terminal, in the project directory:

```bash
# Add a new task
python task_cli.py add "Buy milk"

# Update a task
python task_cli.py update 1 "Buy milk and bread"

# Delete a task
python task_cli.py delete 1

# Mark a task as in progress
python task_cli.py mark-in-progress 1

# Mark a task as done
python task_cli.py mark-done 1

# List all tasks
python task_cli.py list

# List tasks by status
python task_cli.py list done
python task_cli.py list todo
python task_cli.py list in-progress
```

## Task Structure
Each task contains:

- id – unique identifier
- description – a short description of the task
- status – one of: todo, in-progress, done
- createdAt – creation date and time
- updatedAt – last update date and time
- 
## Requirements
Python 3.7+
No external libraries required

Command Line Usage
After setting up the project and adding `task-cli` alias, you can use the CLI tool with commands like:

```bash
task-cli add "Buy groceries"
task-cli list
task-cli mark-done 1
```

