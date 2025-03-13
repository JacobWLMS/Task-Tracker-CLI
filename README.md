# Command-line Todo List App

## Overview
This is a simple command-line task tracker that allows users to add, delete, update, and manage tasks efficiently. The tasks are stored in a `tasks.json` file, and the application provides multiple filtering options to list tasks based on their status.

This project aligns with [this roadmap](https://roadmap.sh/projects/task-tracker) for learning about building a task tracker.

## Features
- Add, delete, and update tasks
- Mark tasks as in progress or completed
- List tasks with different status filters (To-Do, In Progress, Done)
- Save and retrieve tasks from a JSON file
- Displays tasks in a nicely formatted table using `rich`

## Installation
Ensure you have Python installed on your system. This script requires the `rich` package for better output formatting.

### Install dependencies:
```sh
pip install rich
```

## Usage
Run the script using Python:
```sh
python task_tracker.py [OPTIONS]
```

### Task Management
- Add a new task:
  ```sh
  python task_tracker.py -a "Your task description"
  ```
- Delete a task:
  ```sh
  python task_tracker.py -d TASK_ID
  ```
- Update a task description:
  ```sh
  python task_tracker.py -u TASK_ID,"Updated task description"
  ```

### Listing Tasks
- List all tasks:
  ```sh
  python task_tracker.py -l
  ```
- List To-Do tasks:
  ```sh
  python task_tracker.py -lt
  ```
- List In-Progress tasks:
  ```sh
  python task_tracker.py -lp
  ```
- List completed tasks:
  ```sh
  python task_tracker.py -ld
  ```

### Status Management
- Mark a task as in progress:
  ```sh
  python task_tracker.py -p TASK_ID
  ```
- Mark a task as completed:
  ```sh
  python task_tracker.py -c TASK_ID
  ```
- Update task status manually:
  ```sh
  python task_tracker.py -s TASK_ID,STATUS_CODE
  ```
  - `1` = ToDo
  - `2` = InProgress
  - `3` = Done

## Example
Adding a task and marking it as completed:
```sh
python task_tracker.py -a "Finish project documentation"
python task_tracker.py -c 1
```

## Notes
- Tasks are stored in `tasks.json` and persist between runs.
- Ensure to provide valid task IDs when modifying tasks.

