class TaskSetJsonKeys(object):
    # Task set
    KEY_TASKSET = "taskset"

    # Task
    KEY_TASK_ID = "taskId"
    KEY_TASK_PERIOD = "period"
    KEY_TASK_WCET = "wcet"
    KEY_TASK_DEADLINE = "deadline"
    KEY_TASK_OFFSET = "offset"
    KEY_TASK_SECTIONS = "sections"

    # Schedule
    KEY_SCHEDULE_START = "startTime"
    KEY_SCHEDULE_END = "endTime"


class ResourceManagementAlgorithm(object):
    HLP = "HLP"
    NPP = "NPP"
    PIP = "PIP"
    PCP = "PCP"
    SRP = "SRP"


class TaskSetIterator:

    def __init__(self, taskSet):
        self.taskSet = taskSet
        self.index = 0
        self.keys = iter(taskSet.tasks)


    def __next__(self):
        key = next(self.keys)
        return self.taskSet.tasks[key]