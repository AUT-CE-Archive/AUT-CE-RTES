# Standard imports
from typing import Optional

# Third-party imports
from task import Task, TaskState
from taskset import TaskSet


class Scheduler(object):

    def __init__(self, taskset: TaskSet, algorithm: str) -> 'Scheduler':
        self.taskset = taskset

        # Select scheduler based on the specified algorithm
        if algorithm == "edf":
            self.scheduler = self.edf
        elif algorithm == "rm":
            self.scheduler = self.rm
        elif algorithm == "dm":
            self.scheduler = self.dm


    def schedule(self, time: int) -> Optional[Task]:
        """ Schedules tasks and returns the task that that is to be ran at the given time. If None, then no task is to be ran. """
        self.scheduler(time)


    def edf(self, time: int):
        """ Earliest Deadline First (EDF) scheduler """
        print(time)

        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_deadlines = sorted(all_tasks, key=lambda x: x.next_deadline(time))  # Sort tasks by deadlines

        current_task = None
        if time == 21:
            pass

        for task in all_tasks_by_deadlines:

            task.preflight(time)

            # Ignore task if missed deadline
            # if not task.is_complete and task.has_missed_deadline(time):
            #     task.set_state(TaskState.BLOCKED)
            #     task.save_state()
            #     continue

            # If task has not yet been activated
            if not task.is_active:
                if time >= task.act_time:
                    task.set_state(TaskState.READY)
                else:
                    task.set_state(TaskState.NOT_ARRIVED)
                    task.save_state()
                    continue

            # If task is complete
            if not task.has_remaining_time:
                task.set_state(TaskState.COMPLETED)
                task.save_state()
                continue

            # If task is empty and current task is empty, then set current task to task
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)
                task.save_state()
                current_task = task
                continue

            task.set_state(TaskState.READY)
            task.save_state()

        return current_task



    def rm(self, time: int):
        """ Rate Monotonic (RM) scheduler """
        
        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_periods = sorted(all_tasks, key=lambda x: x.period)  # Sort tasks by their periods

        current_task = None
        for task in all_tasks_by_periods:

            task.preflight(time)

            # Complete the task if finished execution
            if not task.has_remaining_time:
                task.set_state(TaskState.COMPLETED)
                task.save_state()
                continue

            # If task is empty and current task is empty, then set current task to task
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)   # Set state to RUNNING (and decrement remaining execution time)
                current_task = task
            elif task.is_active:
                task.set_state(TaskState.READY)     # Set state to READY

            task.save_state()   # Save the state of the task

        return current_task



    def dm(self, time: int):
        """ Deadline Monotonic (DM) scheduler """
        pass