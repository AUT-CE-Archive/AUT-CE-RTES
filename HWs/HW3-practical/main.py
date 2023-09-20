# Standard imports
import json
import sys

# Third-party imports
from src.utils import ResourceManagementAlgorithm
from src.scheduler import Scheduler
from src.taskset import TaskSet


if __name__ == "__main__":

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "taskset_3.json"

    with open(file_path) as json_data:
        data = json.load(json_data)

    # Initialize taskset
    taskSet = TaskSet(data)
    taskSet.printTasks()
    taskSet.printJobs()
    
    # Run scheduler (with verbose)
    print("\nRun:")
    scheduler = Scheduler(
        taskSet=taskSet,
        algorithm=ResourceManagementAlgorithm.HLP,
        verbose=False
    )
    scheduler.run()

    # Timeline
    print("\nTimeline:")
    scheduler.build_timeline()
