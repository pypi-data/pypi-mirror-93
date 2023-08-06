# Shopcloud Metric CLI

## install

```
$ pip install shopcloud_metric
```

## Usage

__Job:__  

Metrics wenn ein Job ausgeführt wird

```py
from shopcloud_metric import JobMetric

job = JobMetric('sage-supplier-update', 
    instance='airflow-production', 
    env='testing',
)
with job as j:
    j.gauge('job_last_success_unixtime', labels={'supplier': 'EP'})
    raise Exception('AS a')
    j.gauge('job_last_success_unixtime', labels={'supplier': 'SP'})

job.gauge('job_last_success_unixtime', labels={'supplier': 'SP'})
job.success()

```

__RawMetrics:__  

```py
from shopcloud_metric import MetricRegistry

registry = MetricRegistry()
registry.gauge('job_up', value=1, labels={'name': 'shopcloud-infrastructure-cli', 'instance': 'tests'})
registry.push()

registry.gauge('job_up', value=0, labels={'name': 'my-job', 'instance': 'airflow-production'})
registry.gauge('job_last_success_unixtime', labels=[{'name': 'test'}])
registry.gauge('api_http_requests_total', value=12, labels={'operation': 'create'})
registry.gauge('process_cpu_seconds_total', value=1)
registry.gauge('http_request_duration_seconds', value=1)
registry.push()
```


### Deploy to PyPi

```sh
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/* 
```