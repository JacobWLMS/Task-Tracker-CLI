import argparse
import os
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def create_parser():
    parser = argparse.ArgumentParser(
        description="Command-line Todo List App",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create argument groups for better organization
    task_group = parser.add_argument_group('Task Management')
    list_group = parser.add_argument_group('List Options')
    status_group = parser.add_argument_group('Status Management')
    
    # Task management options
    task_group.add_argument("-a", "--add", metavar="TASK", help="Add a new task")
    task_group.add_argument("-d", "--delete", metavar="ID", help="Delete a task")
    task_group.add_argument("-u", "--update", metavar="ID,TASK", help="Update a task description")
    
    # List options
    list_group.add_argument("-l", "--list", action="store_true", help="List all tasks")
    list_group.add_argument("-lt", "--list-todo", action="store_true", help="List todo tasks only")
    list_group.add_argument("-lp", "--list-progress", action="store_true", help="List in-progress tasks only")
    list_group.add_argument("-ld", "--list-done", action="store_true", help="List completed tasks only")
    
    # Status management options
    status_group.add_argument("-p", "--progress", metavar="ID", help="Mark task as in progress")
    status_group.add_argument("-c", "--complete", metavar="ID", help="Mark task as completed")
    status_group.add_argument("-s", "--status", metavar="ID,CODE", 
                           help="Update task status (codes: 1=ToDo, 2=InProgress, 3=Done)")
    
    return parser

def add_task(task_description):
    tasks = []
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": task_description,
        "status": "ToDo",
        "lastModified": datetime.now().isoformat()
    }
    
    tasks.append(task)
    
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
    
    console.print(f"[green]Task added:[/green] {task_description}")

def list_tasks(status_filter=None):
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        if tasks:
            filtered_tasks = tasks
            if status_filter:
                filtered_tasks = [t for t in tasks if t['status'] == status_filter]
                
            status_title = status_filter if status_filter else "All"
            table = Table(title=f"Tasks - {status_title}")
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Status", style="magenta")
            table.add_column("Description", style="green")
            for task in filtered_tasks:
                table.add_row(str(task['id']), task['status'], task['description'])
            console.print(table)
        else:
            console.print("[yellow]Task list is empty[/yellow]")
    else:
        console.print("[red]No tasks available[/red]")

def delete_task(task_number):
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        
        try:
            task_number = int(task_number)
            if 1 <= task_number <= len(tasks):
                deleted_task = tasks.pop(task_number-1)
                with open("tasks.json", "w") as file:
                    json.dump(tasks, file, indent=4)
                console.print(f"[red]Deleted task {task_number}:[/red] {deleted_task['description']}")
            else:
                console.print(f"[red]Error: Task number {task_number} does not exist[/red]")
        except ValueError:
            console.print("[red]Error: Task number must be an integer[/red]")
    else:
        console.print("[red]No tasks available[/red]")

def update_task(task_number, task_description):
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        
        try:
            task_number = int(task_number)
            if 1 <= task_number <= len(tasks):
                tasks[task_number-1]['description'] = task_description
                tasks[task_number-1]['lastModified'] = datetime.now().isoformat()
                with open("tasks.json", "w") as file:
                    json.dump(tasks, file, indent=4)
                console.print(f"[blue]Updated task {task_number}:[/blue] {task_description}")
            else:
                console.print(f"[red]Error: Task number {task_number} does not exist[/red]")
        except ValueError:
            console.print("[red]Error: Task number must be an integer[/red]")
    else:
        console.print("[red]No tasks available[/red]")

def update_task_status(task_number, new_status):
    status_map = {
        "1": "ToDo",
        "2": "InProgress", 
        "3": "Done"
    }
    
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        
        try:
            task_number = int(task_number)
            if 1 <= task_number <= len(tasks):
                if new_status in status_map:
                    old_status = tasks[task_number-1]['status']
                    tasks[task_number-1]['status'] = status_map[new_status]
                    tasks[task_number-1]['lastModified'] = datetime.now().isoformat()
                    with open("tasks.json", "w") as file:
                        json.dump(tasks, file, indent=4)
                    console.print(f"[blue]Updated task {task_number} status:[/blue] {old_status} → {status_map[new_status]}")
                else:
                    console.print(f"[red]Error: Invalid status value. Use 1=ToDo, 2=InProgress, 3=Done[/red]")
            else:
                console.print(f"[red]Error: Task number {task_number} does not exist[/red]")
        except ValueError:
            console.print("[red]Error: Task number must be an integer[/red]")
    else:
        console.print("[red]No tasks available[/red]")

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.add:
        task = args.add
        add_task(task)
    elif args.list_todo:
        list_tasks("ToDo")
    elif args.list_progress:
        list_tasks("InProgress")
    elif args.list_done:
        list_tasks("Done")
    elif args.list:
        list_tasks()
    elif args.delete:
        task_number = args.delete
        delete_task(task_number)
    elif args.update:
        try:
            task_number, task = args.update.split(",", 1)
            update_task(task_number, task)
        except ValueError:
            console.print("[red]Error: Update format should be 'ID,TASK'[/red]")
    elif args.progress:
        update_task_status(args.progress, "2")
    elif args.complete:
        update_task_status(args.complete, "3")
    elif args.status:
        try:
            task_number, status = args.status.split(",", 1)
            update_task_status(task_number, status)
        except ValueError:
            console.print("[red]Error: Status format should be 'ID,STATUS'[/red]")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()