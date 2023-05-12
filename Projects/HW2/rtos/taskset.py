# Standard imports
from typing import List

# Third-party imports
from task import Task


class TaskSet(object):

    def __init__(self, tasks: List[Task]) -> 'TaskSet':
        self.tasks = tasks
        self.utility = 0
        self.feaible = False


    def add_task(self, task: Task) -> None:
        """ Add a new task to the task set """
        self.tasks.append(task)


    def get_all_tasks(self) -> List[Task]:
        """ Returns all tasks in the taskset """
        return [task for task in self.tasks]


    def plot_history(self):
        """ Print the history of the task states """
        print("Plotting task history... (RED is for BLOCKED, GREEN is for COMPLETED, BLUE is for RUNNING, WHITE is for READY))")
        for task in self.tasks:
            task.plot_history()