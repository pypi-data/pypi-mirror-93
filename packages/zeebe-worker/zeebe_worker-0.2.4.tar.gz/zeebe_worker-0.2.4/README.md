# Zeebe Worker
A simple Zeebe worker wrapper to let developers focus on what matters.

## Install
`pip install zeebe-worker` or use your preferred package manager.
See https://pypi.org/project/zeebe-worker/#history for available versions.

## Usage
```python
from zeebe_worker import ZeebeWorker
from extensions import zeebe_stub
from config import worker_name

class MyWorker(ZeebeWorker):

    def my_task_type_handler(self, job):
        """Handling my_task_type
        """
        variables = json.loads(job.variables)
        if something_fails:
            # This will trigger a FailJobRequest with the exception
            raise Exception
        return variables

    def another_task_type_handler(self, job):
        """Handles another task
        """
        # This will always succeed as an exception will never be raised
        pass


# Create your own class instance with your own configuration
my_worker = MyWorker(zeebe_stub, worker_name)

# Subscribe to a task type (uses threading.Thread for concurrency)
my_worker.subscribe('my_task_type', 'my_task_type_handler')
my_worker.subscribe('my-task-typo', 'my_task_type_handler')
my_worker.subscribe('another_task_type', 'another_task_type_handler')
```

## API
### `ZeebeWorker.__init__`
Initiates the worker class with the set defaults.

| arg | desc | default |
| --- | ---- | ------- |
| stub | The grpc stub to connect to Zeebe with | - |
| worker_name | The worker_name to send to along to Zeebe (mainly for debugging purposes) | - |
| timeout | Number of milliseconds for a job to timeout | 5\*60\*1000 (5 minutes) |
| request_timeout | Long polling: number of milliseconds for an ActivateJobs request to timeout | 1\*60\*1000 (1 minute) |
| max_jobs_to_activate | Maximum amount of jobs to activate in one request | 1 |
| backoff_interval | Number of milliseconds to backoff when unable to reach Zeebe | 5\*1000 (5 seconds) |

### `ZeebeWorker.subscribe`
Subscribes the target to the task type concurrently.

| arg | desc | default |
| --- | ---- | ------- |
| task_type | The task or job type to subscribe to | - |
| target | The function to execute. When using a string, it will convert that to the method within the current class | - |
| timeout | Number of milliseconds for the jobs which are activated to timeout | set at class instantiation |
| request_timeout | Number of milliseconds for the ActivateJobs request to timeout | set at class instantiation |
| max_jobs_to_activate | Maximum amount of jobs to activate in one request | set at class instantiation |
| autocomplete | Complete jobs when the handler returns a non-error | False |
| backoff_interval | Number of milliseconds to backoff when unable to reach Zeebe | set at class instantiation |

## Target functions
Your own target function must accept one argument, preferably called `job`. This will be provided
as Zeebe's `ActivatedJob` ([ref](https://docs.zeebe.io/reference/grpc.html#output-activatejobsresponse)).
Extract the variables using `variables = json.loads(job.variables)`.

### Fail a job
Raising **any exception** in the function will send a FailJobRequest to zeebe with the raised exception.

### Complete a job
A CompleteJobRequest will be sent for the job if the function excecutes without raising an exception.

#### Setting variables
When the function returns a dict, it will send this dict as variables with the CompleteJobRequest.

## Compatability

| Zeebe Worker | Zeebe |
| --- | --- |
| 0.2.x | >= 0.23 |
| 0.1.0 | 0.22.1 |
