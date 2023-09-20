# Third-party imports
from src.job import Job
from src.utils import TaskSetJsonKeys


class Task(object):

    def __init__(self, taskDict: dict) -> 'Task':
        """
            Constructor

            Parameters:
                taskDict (dict): Dictionary containing task information
        """
        self.id = int(taskDict[TaskSetJsonKeys.KEY_TASK_ID])
        self.period = float(taskDict[TaskSetJsonKeys.KEY_TASK_PERIOD])
        self.wcet = float(taskDict[TaskSetJsonKeys.KEY_TASK_WCET])
        self.relativeDeadline = float(taskDict.get(TaskSetJsonKeys.KEY_TASK_DEADLINE, taskDict[TaskSetJsonKeys.KEY_TASK_PERIOD]))
        self.offset = float(taskDict.get(TaskSetJsonKeys.KEY_TASK_OFFSET, 0.0))
        self.sections = taskDict[TaskSetJsonKeys.KEY_TASK_SECTIONS]

        self.lastJobId = 0
        self.lastReleasedTime = 0.0
        self.jobs = []


    def getAllResources(self):
        pass


    def spawnJob(self, releaseTime: float) -> Job|None:
        """
            Spawns a job if release time is reached for the task

            Parameters:
                releaseTime (float): Time of the release
            Returns:
                (Job|None) Job instance if conditions are met, None otherwise
        """
        if self.lastReleasedTime > 0 and releaseTime < self.lastReleasedTime:
            print("INVALID: release time of job is not monotonic")
            return None

        if self.lastReleasedTime > 0 and releaseTime < self.lastReleasedTime + self.period:
            print("INVDALID: release times are not separated by period")
            return None

        self.lastJobId += 1
        self.lastReleasedTime = releaseTime

        job = Job(self, self.lastJobId, releaseTime)
        self.jobs.append(job)
        return job


    def getJobs(self) -> list:
        """ Return list of job instances """
        return self.jobs


    def getJobById(self, jobId: int) -> Job|None:
        """
            Returns a job intance givemn its ID

            Parameters:
                jobId (int): ID of the job to retreive
            Returns:
                (Job|None) Job instance if found, None otherwise
        """

        # Return Null if ID is not valid
        if jobId > self.lastJobId:
            return None

        job = self.jobs[jobId - 1]
        if job.id == jobId:
            return job

        for job in self.jobs:
            if job.id == jobId:
                return job

        return None


    def getUtilization(self) -> float:
        """ Returns the utilization for the task """
        return self.wcet / self.period


    def __str__(self):
        return f"task {self.id}: (Φ,T,C,D,∆) = ({self.offset}, {self.period}, {self.wcet}, {self.relativeDeadline}, {self.sections})"


    def __repr__(self):
        return f"task {self.id}: (Φ,T,C,D,∆) = ({self.offset}, {self.period}, {self.wcet}, {self.relativeDeadline}, {self.sections})"