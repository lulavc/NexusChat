from typing import Dict, List
from dataclasses import dataclass

@dataclass
class DevelopmentTask:
    task_id: str
    description: str
    depends_on: List[str]
    implementation_file: str
    test_files: List[str]
    docs: List[str]

class TaskGraph:
    def __init__(self):
        self.tasks: Dict[str, DevelopmentTask] = {}

    def add_task(self, task: DevelopmentTask):
        self.tasks[task.task_id] = task

    def get_next_tasks(self, completed_id: str) -> List[DevelopmentTask]:
        return [t for t in self.tasks.values() 
                if completed_id in t.depends_on]
