import csv
from task import Task
from task_set import TaskSet
from RTOS import RTOS
from schedular import Scheduler
from printer import TaskSetPrinter as Printer


class Main:
    def __init__(self):
        self.rtos = RTOS()
        self.task_set = TaskSet()

    def run(self):
        # create tasks and add them to task set
        self.read_tasks_from_csv('tasks1.csv')

        # schedule tasks using EDF algorithm
        self.rtos.set_task_set(self.task_set)
        # you need to find hyper period and change duration to hyper period
        duration = 350
        self.rtos.run(duration)

    def read_tasks_from_csv(self, filename):
        with open(filename, 'r') as csvfile:
            # header in csv file: priority,name,  state, type, act_time, period, wcet, deadline
            taskreader = csv.reader(csvfile, delimiter=',',)
            next(taskreader, None)  # skip the headers
            for row in taskreader:
                priority, name,  state, type, act_time, period, wcet, deadline = row
                print(f"priority: {priority}\t\tname: {name}\t\tstate: {state}\t\ttype: {type}\t\tact_time: {act_time}\t\tperiod: {period}\t\twcet: {wcet}\t\tdeadline: {deadline}")
                task = Task(
                    priority=int(priority),
                    name=name,
                    state=int(state),
                    type=int(type),
                    act_time=int(act_time),
                    period=int(period),
                    wcet=int(wcet),
                    deadline=int(deadline)
                )
                self.task_set.add_task(task)


if __name__ == '__main__':
    main = Main()
    main.run()
