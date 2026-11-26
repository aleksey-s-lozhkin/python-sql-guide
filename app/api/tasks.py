"""Задачи практики: YAML-файлы в app/data/tasks."""
from dataclasses import dataclass, field
from typing import List, Optional

import yaml

from .settings import TASKS_DIR


@dataclass
class Task:
    slug: str
    title: str
    prompt: str
    reference: str
    chapter: str = ""
    difficulty: str = ""
    hints: List[str] = field(default_factory=list)
    ordered: bool = False
    order: int = 100


_tasks = {}
_loaded = False


def _read_one(path) -> Task:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    required = ("slug", "title", "prompt", "reference")
    for key in required:
        if not data.get(key):
            raise ValueError("В задаче {} нет поля {}".format(path.name, key))
    return Task(
        slug=data["slug"],
        title=data["title"],
        prompt=data["prompt"].strip(),
        reference=data["reference"].strip(),
        chapter=str(data.get("chapter", "")),
        difficulty=str(data.get("difficulty", "")),
        hints=[str(h) for h in data.get("hints", [])],
        ordered=bool(data.get("ordered", False)),
        order=int(data.get("order", 100)),
    )


def load_tasks() -> None:
    global _loaded
    _tasks.clear()
    for path in sorted(TASKS_DIR.glob("*.yaml")):
        task = _read_one(path)
        _tasks[task.slug] = task
    _loaded = True


def all_tasks() -> List[Task]:
    return sorted(_tasks.values(), key=lambda t: (t.order, t.title))


def get_task(slug: str) -> Optional[Task]:
    return _tasks.get(slug)


def public_task(task: Task) -> dict:
    return {
        "slug": task.slug,
        "title": task.title,
        "prompt": task.prompt,
        "chapter": task.chapter,
        "difficulty": task.difficulty,
        "hints": task.hints,
    }


def task_list(task: Task) -> dict:
    return {
        "slug": task.slug,
        "title": task.title,
        "chapter": task.chapter,
        "difficulty": task.difficulty,
    }
