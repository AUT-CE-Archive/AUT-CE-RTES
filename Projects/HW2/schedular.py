from task import *
from task_set import TaskSet


class Scheduler:
    """Scheduler Class

    Attributes:
        task_set (TaskSet): Task set to be scheduled
    """

    def __init__(self, task_set: TaskSet):
        self.task_set = task_set
        self.completed_tasks = []

    def get_ready_tasks(self):
        """Get a list of all ready tasks in the task set

        Returns:
            list: List of all Task objects in the task set that are in the READY state
        """
        ready_tasks = []
        for task in self.task_set.get_all_tasks():
            if task.state == READY:
                ready_tasks.append(task)
        return ready_tasks

    def schedule(self):
        """Schedule the next task to run

        Returns:
            Task: The next task to run, or None if no tasks are ready
        """
        # complete here

        ready_tasks = self.get_ready_tasks()
        if not ready_tasks:
            return None
        highest_priority = min([task.priority for task in ready_tasks])
        highest_priority_tasks = [task for task in ready_tasks if task.priority == highest_priority]
        return highest_priority_tasks[0]

    def set_task_set(self, task_set):
        """Set the task set for the scheduler

        Args:
            task_set (TaskSet): The task set to be scheduled
        """
        self.task_set = task_set


    def edf(self):
        completed_tasks = []

        # Get READY tasks
        ready_tasks = self.get_ready_tasks()

        # Get tasks with earliest deadline
        earliest_deadline = min([task.deadline for task in ready_tasks])
        earliest_deadline_tasks = [task for task in ready_tasks if task.deadline == earliest_deadline]

        earliest_deadline_tasks[0].wcet -= 1    # 


        earliest_deadline = min([task.deadline for task in ready_tasks])
        earliest_deadline_tasks = [task for task in ready_tasks if task.deadline == earliest_deadline]
        return earliest_deadline_tasks[0]