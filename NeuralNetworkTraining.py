import datetime
import pickle
from random import shuffle

import ray
from ray.job_submission import JobStatus
import time

from Board import Board
from Samurai import Samurai


def train_controller_list(controller_list, jobs_client, num_loops=1000, num_agents=10):
    # Function to run the training of agents from a list of available agents
    loops_completed = 0
    # Variable to track the number of loops completed
    create_runtime_file(num_agents, controller_list)
    timedate = f"{datetime.datetime.date}-{datetime.datetime.hour}-{datetime.datetime.minute}-{datetime.datetime.second}"
    print(timedate)
    while loops_completed < num_loops:
        # Runs for a number of loops as input, or 1000 by default
        jobs_client.submit_job(
            entrypoint="python RunTrainingRound.py",
            # Path to the local directory that contains the script.py file
            runtime_env={"working_dir": "./"}
        )
        # Submits the job to the jobs client using the RunTrainingRound.py script
        loops_completed += 1
        wait_until_status(job_id, jobs_client, {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED})
        logs = jobs_client.get_job_logs(job_id)
        print(logs)


def wait_until_status(job_id, client, status_to_wait_for):
    status_list = []
    while True:
        status = client.get_job_status(job_id)
        if status not in status_list:
            print(f"status: {status}")
            status_list += [status]
        if status in status_to_wait_for:
            break
        time.sleep(1)


def create_runtime_file(num_agents, controller_list):
    runtime_pickle_address = 'runtime_data.pickle'
    stored_dict = {'num_agents': num_agents, 'controller_list': controller_list}
    with open(runtime_pickle_address, 'wb') as file:
        pickle.dump(stored_dict, file)


def read_runtime_file():
    runtime_pickle_address = 'runtime_data.pickle'
    with open(runtime_pickle_address, 'rb') as file:
        data_dict = pickle.load(file)

    return data_dict['num_agents'], data_dict['controller_list']
