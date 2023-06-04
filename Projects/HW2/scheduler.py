# Standard imports
from typing import Optional

# Third-party imports
from task import Task, TaskState
from taskset import TaskSet


class Scheduler(object):

    def __init__(self, taskset: TaskSet, algorithm: str) -> 'Scheduler':
        self.taskset = taskset
        self.taskset.algorithm = algorithm
        self.scheduler = {
            "edf_preemptive": self.edf_preemptive,
            "edf_non_preemptive": self.edf_non_preemptive,
            "rm": self.rm,
            "dm": self.dm
        }[algorithm]


    def schedule(self, time: int) -> Optional[Task]:
        """ Schedules tasks and returns the task that that is to be ran at the given time. If None, then no task is to be ran. """
        self.scheduler(time)


    def edf_preemptive(self, time: int):
        """ Preemptive Earliest Deadline First (EDF) scheduler """

        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_deadlines = sorted(all_tasks, key=lambda x: x.next_deadline(time))  # Sort tasks by deadlines

        current_task = None
        for task in all_tasks_by_deadlines:
            task.preflight(time)

            # Interrupt (very hard deadline)
            if task.is_ready and current_task is None and task.is_type_interrupt:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # EDF doesn't really care about the type of the task
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)
                current_task = task

            task.save_state()   # Save the state of the task

        return current_task


    def edf_non_preemptive(self, time: int):
        """ None Preemptive Earliest Deadline First (EDF) scheduler """

        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_deadlines = sorted(all_tasks, key=lambda x: x.next_deadline(time))  # Sort tasks by deadlines

        # Continue current running task
        current_task = None
        for task in all_tasks_by_deadlines:
            task.preflight(time)
            if task.is_running:
                task.set_state(TaskState.RUNNING)   # Manually decrement ramaining_time
                return task

        for task in all_tasks_by_deadlines:
            task.preflight(time)

            # Interrupt (very hard deadline)
            if task.is_ready and current_task is None and task.is_type_interrupt:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # EDF doesn't really care about the type of the task
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)
                current_task = task

            task.save_state()   # Save the state of the task

        return current_task


    def rm(self, time: int):
        """ Rate Monotonic (RM) scheduler """
        
        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_periods = sorted(all_tasks, key=lambda x: x.period)  # Sort tasks by their periods

        current_task = None
        for task in all_tasks_by_periods: 
            task.preflight(time)

            # Interrupt (very hard deadline)
            if task.is_ready and current_task is None and task.is_type_interrupt:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # Sporadic (harder deadline)
            if task.is_ready and current_task is None and task.is_type_sporadic:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # Periodic or aperiodic tasks (no clear indication which has higher priority!)
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)
                current_task = task

            task.save_state()   # Save the state of the task

        return current_task


    def dm(self, time: int):
        """ Deadline Monotonic (DM) scheduler """

        all_tasks = self.taskset.get_all_tasks()    # Get ready tasks
        all_tasks_by_deadlines = sorted(all_tasks, key=lambda x: x.next_deadline(time))  # Sort tasks by deadlines

        current_task = None
        for task in all_tasks_by_deadlines:
            if time >= 21:
                print(end="")
            task.preflight(time)

            # Interrupt (very hard deadline)
            if task.is_ready and current_task is None and task.is_type_interrupt:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # Sporadic (harder deadline)
            if task.is_ready and current_task is None and task.is_type_sporadic:
                task.set_state(TaskState.RUNNING, save=True)
                current_task = task
                continue

            # Sporadic, aperiodic or periodic (EDF doesn't really care about the type of the task)
            if (task.is_ready or task.is_running) and current_task is None:
                task.set_state(TaskState.RUNNING)
                current_task = task

            task.save_state()   # Save the state of the task

        return current_task
