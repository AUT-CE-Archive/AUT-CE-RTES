# Standard imports
from pandas import DataFrame, read_csv
from typing import List

# Third-party imports
from task import Task, TaskState, TaskType
from taskset import TaskSet
from scheduler import Scheduler


def read_taskset(path: str) -> DataFrame:
    """ Reads a task set from a csv file and returns a pandas DataFrame """
    return read_csv(path)


def build_tasks(df: DataFrame) -> List[Task]:
    """ Builds a list of tasks from a pandas DataFrame """
    tasks = []
    for _, task in df.iterrows():
        tasks.append(
            Task(
                name=task['name'],
                state=TaskState.NOT_ARRIVED,
                type=TaskType(task['type']),
                act_time=task['act_time'],
                period=task['period'],
                wcet=task['wcet'],
                deadline=task['deadline']
            )
        )
    return tasks


DURATION = 100


if __name__ == '__main__':

    # Read CSV
    tasks_df = read_taskset("data/tasks1.csv")
    # tasks_df = read_taskset("data/tasks2.csv")
    # tasks_df = read_taskset("data/tasks_interrupts.csv")

    # Initialize scheduler
    for algorithm in ["dm", "rm", "edf_preemptive", "edf_non_preemptive"]:
        tasks = build_tasks(tasks_df)
        taskset = TaskSet(tasks)
        scheduler = Scheduler(taskset, algorithm)

        # Run RTOS
        for time in range(DURATION):
            next_task = scheduler.schedule(time)

        # Plot task history
        taskset.plot_history()
