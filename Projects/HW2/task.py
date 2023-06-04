# Standard imports
from typing import Optional
from enum import Enum

# Third-party imports
from utils import *


class TaskState(Enum):
    RUNNING = 0         # Currently executing on the processor
    READY = 1           # Ready to run but task of higher or equal priority is currently running
    BLOCKED = 2         # Task is waiting for some condition to be met to move to READY state
    SUSPENDED = 3       # Task is waiting for some other task to unsuspend
    COMPLETED = 4       # Task has completed execution
    NOT_ARRIVED = 5     # Task has not arrived yet


class TaskType(Enum):
    INTERRUPT = 0       # Task type is interrupt (hard deadline)
    PERIODIC = 1        # Task type is periodic (hard deadline)
    APERIODIC = 2       # Task type is aperiodic (soft deadline)
    SPORADIC = 3        # Task type is sporadic (hard deadline)


class Task(object):

    def __init__(self,
                 name: str,
                 state: TaskState = TaskState.NOT_ARRIVED,
                 type: TaskType = TaskType.INTERRUPT,
                 act_time: int = 0,
                 period: int = 0,
                 wcet: int = 0,
                 deadline: int = 1000
                 ) -> 'Task':
        self.name = name
        self.state = state
        self.type = type
        self.act_time = act_time
        self.period = period
        self.wcet = wcet
        self.daedline = deadline

        self.remaining_time = wcet      # Remaining execution time
        self.history = []               # Store 'TaskState' per time unit


    def set_state(self, state: TaskState, save: bool = False, decrement: bool = True) -> None:
        """ Set the state of the task """
        self.state = state
        if save: self.save_state()

        # Decrement remaining execution time if task is running
        if decrement and state == TaskState.RUNNING:
            self.remaining_time -= 1


    def save_state(self) -> None:
        """ Save the current state of the task """
        self.history.append(self.state)


    def plot_history(self):
        """ Print the history of the task states """
        print(f"{self.name}:", end = '\t')
        for state in self.history:
            if state == TaskState.RUNNING:
                blue("▉")
            elif state == TaskState.READY:
                white("▉")
            elif state == TaskState.COMPLETED:
                green("▉")
            elif state == TaskState.BLOCKED:
                red("▉")
            elif state == TaskState.SUSPENDED:
                yellow("▉")
            elif state == TaskState.NOT_ARRIVED:
                black("▉")
        print("")


    def next_deadline(self, time: int) -> Optional[int]:
        """ Returns the next deadline of the task (deadline of a periodic task is its next period) """
        if self.is_periodic:
            if time % self.period == 0:
                deadline = self.act_time + (time // self.period) * self.period
            else:
                deadline = self.act_time + (time // self.period + 1) * self.period
        else:
            deadline = self.act_time + self.daedline
        return deadline


    def preflight(self, time: int):
        """ Perform preflight checks on the task """

        # Reset WCET if task is periodic
        if self.is_periodic and time >= self.period and time % self.period == 1:
            self.remaining_time = self.wcet

        # Set state as ready if task has arrived (should be before other state checks)
        if time >= self.act_time:
            self.set_state(TaskState.READY)

        # Set state as completed if task has no remaining execution time
        if self.remaining_time == 0:
            self.set_state(TaskState.COMPLETED)


    def has_missed_deadline(self, time: int) -> bool:
        """ Returns True if the task has missed its deadline """
        return self.next_deadline(time) < time

    @property
    def is_running(self) -> bool:
        """ Returns True if the task is currently running on the processor """
        return self.state == TaskState.RUNNING

    @property
    def is_complete(self) -> bool:
        """ Returns True if the task has completed execution """
        return self.state == TaskState.COMPLETED

    @property
    def is_ready(self) -> bool:
        """ Returns True if the task is ready to run """
        return self.state == TaskState.READY

    @property
    def is_periodic(self) -> bool:
        """ Returns True if the task is periodic """
        return self.type == TaskType.PERIODIC

    @property
    def is_active(self) -> bool:
        """ Returns True if the task has arrived """
        return self.state != TaskState.NOT_ARRIVED

    @property
    def is_type_interrupt(self) -> bool:
        """ Returns True if task is of type interrupt """
        return self.type == TaskType.INTERRUPT

    @property
    def is_type_sporadic(self) -> bool:
        """ Return Truew if task is of type sporadic """
        return self.type == TaskType.SPORADIC

    @property
    def is_type_aperiodic(self) -> bool:
        """ Return True if task is of type aperiodic """
        return self.type == TaskType.APERIODIC

    @property
    def is_type_periodic(self) -> bool:
        """ Return True if task is of type periodic """
        return self.type == TaskType.PERIODIC

    @property
    def has_remaining_time(self) -> bool:
        """ Returns True if the task has remaining execution time """
        return self.remaining_time > 0
