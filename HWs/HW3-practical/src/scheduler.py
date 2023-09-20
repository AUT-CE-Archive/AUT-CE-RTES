# Standard imports
from typing import List

# Third-party imports
from src.job import Job
from src.taskset import TaskSet
from src.utils import ResourceManagementAlgorithm


class Scheduler(object):

    def __init__(self, taskSet: TaskSet, algorithm: ResourceManagementAlgorithm, verbose: bool = False):
        """
            Constructor

            Parameters:
                taskSet (TaskSet): Task set instance
                algorithm (ResourceManagementAlgorithm): Resource management algorithm
                verbose (bool): If True, scheduler logs will be printed out as it runs
        """
        self.algorithm = algorithm
        self.taskSet = taskSet
        self.time = taskSet.startTime   # Universal time of the scheduler
        self.verbose = verbose

        self.latest_job = None
        self.active_jobs = []
        self.history = []               # To keep what happened within the scheduler


    def run(self):
        """ Main event loop that runs until completion """
        while self.time <= self.taskSet.endTime and self.active_jobs is not None:
            self.tick()


    def get_active_jobs(self) -> List[Job]:
        """ Returns a list of Jobs that are neither complete, nor passed """
        return [job for job in self.taskSet.jobs if job.isActive(self.time) and not job.isCompleted()]


    def get_semaphore_priority(self, semaphore_id: int) -> int:
        """ Returns priority for the given semaphore ID based on the algorithm """
        return {
            ResourceManagementAlgorithm.NPP: 0,
            ResourceManagementAlgorithm.HLP: self.taskSet.lowest_priority_semaphores[semaphore_id],
        }[self.algorithm]


    def tick(self):

        # Get list of active jobs to run
        self.active_jobs = self.get_active_jobs()

        # Increment clock
        self.time += 1

        if len(self.active_jobs) == 0:
            # Nore more work! We happy
            self.latest_job = None
            self.history.append({
                "task": None,
                "job": None,
                "section": None,
                "priority": None,
            })
            return

        # Set priority to initial pririty if job is about to start
        if self.latest_job and not self.latest_job.isCompleted():
            if self.latest_job.nextSectionJustStarted():
                self.latest_job.priority = self.latest_job.ip

        # Get the job to run sorted by priotity and release time
        self.active_jobs.sort(key=lambda job: (job.priority, job.releaseTime), reverse=True)
        active_job = self.active_jobs[-1]
        held_section = active_job.getResourceHeld()
        active_job.execute(1)   # Execute job by 1 tick

        # Aquire the task
        if held_section != 0:
            # new task is asking for semaphore, bump priority
            active_job.priority = self.get_semaphore_priority(held_section)

        self.history.append({
                "task": active_job.task.id,
                "job": active_job.id,
                "section": held_section,
                "priority": active_job.priority
        })
        self.latest_job = active_job

        # Job is done!
        if active_job.isCompleted():
            is_missed = self.time >= active_job.deadline
            deadline_status = f"{'MISSED' if is_missed else 'MET'} DEADLINE"
            print(f"JOB {active_job.id} of TASK {active_job.task.id} COMPLETED AT {self.time} ({deadline_status})")


        if self.verbose:
            print(f"TIME {self.time - 1}) {self.history[-1]}")


    def build_timeline(self):
        time = self.taskSet.startTime
        # First item in history is initially active
        active_job_signature = f"{self.history[0]['task']}-{self.history[0]['job']}-{self.history[0]['section']}"
        active_job_is_idle = (self.history[0]['task'] is None)

        for _time, info in enumerate(self.history):
            # Get history signature and idle status
            signature = f"{info['task']}-{info['job']}-{info['section']}"
            is_idle = (info['task'] is None)

            # New task/job/section
            if signature != active_job_signature:
                print(f"{time} - {_time}:\t{f'{active_job_signature}' if not active_job_is_idle else 'IDLE'}")
                # Set it as active
                time = _time
                active_job_signature = signature
                active_job_is_idle = is_idle

        # IDLE when all tasks are done
        print(f"{time} - {self.taskSet.endTime}:\tIDLE")
