"""To-do list stored in data/todos.json (persists between runs)."""
import json
import os
import re

DATA_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "todos.json"))


def _load():
    try:
        with open(DATA_FILE, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def _save(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(tasks, fh, indent=2, ensure_ascii=False)


def get_tasks():
    """Return the saved tasks as a list of strings."""
    return _load()


def parse_task(text):
    """Strip command words such as 'add', 'todo add', 'remind me to'."""
    task = re.sub(r"^\s*(please\s+)?(todo\s+add|add\s+task|add|new\s+todo|new\s+task|remind\s+me\s+to|todo)\s*(to\s+)?",
                  "", text, flags=re.I)
    return re.sub(r"\s+to\s+(my\s+)?(list|todo.*|tasks?)$", "", task, flags=re.I).strip()


def add_item(task):
    """Append a task exactly as given (used by the web UI)."""
    task = task.strip()
    if not task:
        return "What should I add? e.g. 'todo add finish lab record'."
    tasks = _load()
    tasks.append(task)
    _save(tasks)
    return f"Added: '{task}'  (you now have {len(tasks)} task(s))"


def add_task(text):
    """Add a task from a chat command; command words like 'add' are stripped first."""
    return add_item(parse_task(text))


def list_tasks():
    tasks = _load()
    if not tasks:
        return "Your to-do list is empty. Try 'todo add <task>'."
    lines = ["Your tasks:"] + [f"   {i}. {t}" for i, t in enumerate(tasks, 1)]
    return "\n".join(lines)


def remove_task(text):
    match = re.search(r"\d+", text)
    tasks = _load()
    if not match:
        return "Tell me the task number, e.g. 'todo remove 1'."
    n = int(match.group())
    if not 1 <= n <= len(tasks):
        return f"No task number {n}. You have {len(tasks)} task(s)."
    removed = tasks.pop(n - 1)
    _save(tasks)
    return f"Removed task {n}: '{removed}'"
