# Third-party imports
# from src.task import Task


class Job(object):

    def __init__(self, task, jobId: int, releaseTime: float) -> 'Job':
        """
            Constructor

            Parameters:
                task (Task): Parent task instance
                jobId (int): Unique job ID
                releaseTime (float): Release time of the job
        """
        self.task = task
        self.id = jobId
        self.releaseTime = releaseTime                  # Same as release time of task
        self.relativeDeadline = task.relativeDeadline   # Same as relative deadline of task
        self.remainingTime = task.wcet                  # Same as WCET on initialization

        self.executedTime = 0
        self.ip = None          # IP stands for Initial Priority, initialized based on relative Deadlines
        self.priority = None    # Priority is more dynamic and can change based on the current state of tasks and the scheduler
        self.init_priority_DM() # ip = priority


    def init_priority_DM(self):
        """ Initializes priorities for DM scheduler """
        self.ip = self.priority = self.task.relativeDeadline


    def nextSectionJustStarted(self) -> bool:
        executedTime = self.executedTime

        for _, section in enumerate(self.task.sections):
            section_duration = section[1]
            if executedTime < section_duration:
                # Section is being held and have not fully been executed
                break

            executedTime -= section_duration   # Resouce can be fully consumed
        return executedTime == 0


    def getResourceHeld(self) -> int:
        """ Returns the ID of the resource that it's currently holding """
        executedTime = self.executedTime
        last_semaphore = self.task.sections[0][0]

        for _, section in enumerate(self.task.sections):
            section_duration = section[1]
            if executedTime < section_duration:
                # Section is being held and have not fully been executed
                break

            executedTime -= section_duration   # Resouce can be fully consumed
            last_semaphore = self.task.sections[_ + 1][0]
        return last_semaphore


    def getRecourseWaiting(self):
        '''a resource that is being waited on, but not currently executing'''
        "@TODO"
        pass


    def getRemainingSectionTime(self):
        "@TODO"
        pass


    def execute(self, time: int) -> None:
        """
            Executes the job for the given time

            Parameters:
                time (int): Time to execute the job
            Returns:
                None
        """
        self.remainingTime -= time
        self.executedTime += time


    def executeToCompletion(self) -> None:
        """ Executes the job to completion on the remaining time """
        self.execute(self.remainingTime)


    def isCompleted(self) -> bool:
        """ Returns True if the job is completed, False otherwise """
        return self.remainingTime <= 0


    def isActive(self, time: float) -> bool:
        """ Returns True if release time has not yet been reached, False otherwise """
        return self.releaseTime <= time


    @property
    def deadline(self) -> float:
        return self.releaseTime + self.relativeDeadline


    def __str__(self):
        return f"[{self.task.id}:{self.id}] released at {self.releaseTime} -> deadline at {self.deadline}"


    def __repr__(self):
        return f"[{self.task.id}:{self.id}] released at {self.releaseTime} -> deadline at {self.deadline}"
