# Third-party imports
from src.task import Task
from src.utils import TaskSetJsonKeys, TaskSetIterator



class TaskSet(object):

    def __init__(self, data: dict) -> 'TaskSet':

        self.tasks = {}
        self.jobs = []

        # Retreive start and end times for the taskset
        self.startTime = int(data[TaskSetJsonKeys.KEY_SCHEDULE_START])
        self.endTime = int(data[TaskSetJsonKeys.KEY_SCHEDULE_END])

        self.parseDataToTasks(data)
        self.buildJobReleases()

        self.lowest_priority_semaphores = self.build_lowest_priority_semaphores()


    def build_lowest_priority_semaphores(self):
        """
            This method builds a dictionary for Semaphores with lowest priorities (highest relative deadlines)
        """
        semaphore_priorities = {}
        for task in self:
            for section in task.sections:
                semaphore_id = section[0]
                semaphore_duration = section[1]

                # Ignore secrion if ID is 0
                if semaphore_id == 0:
                    continue

                if semaphore_id not in semaphore_priorities:
                    # Unseen sections
                    semaphore_priorities[semaphore_id] = task.jobs[0].ip
                elif task.jobs[0].ip < semaphore_priorities[semaphore_id]:
                    # Sections with lower priority
                    semaphore_priorities[semaphore_id] = task.jobs[0].priority
        return semaphore_priorities


    def parseDataToTasks(self, data: dict) -> None:
        """
            Parses tasks from the give dictionary and creates a dictionary of tasks

            Parameters:
                data (dict): JSON file dictionary
            Returns:
                None
        """
        for taskData in data[TaskSetJsonKeys.KEY_TASKSET]:
            task = Task(taskData)
            self.tasks[task.id] = task


    def buildJobReleases(self):
        """ Builds jobs """
        for task in self:
            # Find the real time at which the task starts
            t = max(task.offset, self.startTime)

            # Build jobs according to tasks
            while t < self.endTime:
                job = task.spawnJob(t)
                if job:
                    self.jobs.append(job)
                t += task.period


    def __contains__(self, elt):
        return elt in self.tasks


    def __iter__(self):
        return TaskSetIterator(self)


    def __len__(self):
        return len(self.tasks)


    def getTaskById(self, taskId: int):
        """ Returns a task by its ID """
        return self.tasks[taskId]


    def printTasks(self):
        """ Prints all the tasks """
        print("\nTask Set:")
        for task in self:
            print(task)


    def printJobs(self):
        """ Prints all the jobs """
        print("\nJobs:")
        for task in self:
            for job in task.getJobs():
                print(job)
