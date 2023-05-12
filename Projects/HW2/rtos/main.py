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


DURATION = 350


if __name__ == '__main__':

    # Read CSV
    tasks_df = read_taskset("data/tasks3.csv")

    # Initialize tasks
    tasks = build_tasks(tasks_df)

    # Initialize task set
    taskset = TaskSet(tasks)

    # Initialize scheduler
    scheduler = Scheduler(taskset, "edf")

    # Run RTOS
    for time in range(DURATION):
        next_task = scheduler.schedule(time)

        if next_task is None:
            pass


        taskset.plot_history()
