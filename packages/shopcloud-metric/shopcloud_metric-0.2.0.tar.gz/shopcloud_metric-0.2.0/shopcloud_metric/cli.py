import requests
import os
import time
from datetime import datetime
from shopcloud_secrethub import SecretHub


class Gauge:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.value = kwargs.get('value')
        if self.value is None and "_unixtime" in self.name:
            self.value = int(datetime.utcnow().strftime('%s'))
        self.labels = kwargs.get('labels', {})

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
            'labels': self.labels,
        }


class MetricRegistry:
    """
    registry = MetricRegistry()
    registry.gauge('job_up', value=0, labels={'name': 'my-job', 'instance': 'airflow-production'})
    registry.gauge('job_last_success_unixtime', labels={'name': 'test'}]
    registry.gauge('api_http_requests_total', value=12, labels={'operation': 'create'})
    registry.gauge('process_cpu_seconds_total', value=1)
    registry.gauge('http_request_duration_seconds', value=1)
    registry.push()
    """

    def __init__(self, **kwargs):
        self.env = kwargs.get('env', 'production')
        self.metrics = []
        self.labels = kwargs.get('labels', {})
        self.hub = SecretHub(
            user_app='kpi-signal', 
            api_token=os.environ.get('SECRETHUB_TOKEN')
        )

    def gauge(self, name: str, **kwargs):
        labels = kwargs.get('labels', {})
        for key in self.labels.keys():
            labels[key] = self.labels[key]
        self.metrics.append(
            Gauge(
                name, 
                value=kwargs.get('value'), 
                labels=labels,
            )
        )

    def _push(self, metrics: list):
        if self.env == "testing":
            print('push-metrics: {}'.format(metrics))
            return True
        response = requests.post(
            'https://europe-west3-shopcloud-analytics.cloudfunctions.net/metric-gateway-api',
            headers={
                'User-Agent': 'shopcloud-infrastructure',
                'auth': self.hub.read('talk-point/kpi-gateway/auth-token')
            },
            json={
                'metrics': metrics
            }
        )
        print('metric-gateway-api status_code: {} content: {}'.format(response.status_code, response.content))
        return (200 <= response.status_code <= 299)

        return True

    def push(self):
        metrics = [x.to_dict() for x in self.metrics]
        
        is_success = False
        for i in range(10): # 
            response_is_success = self._push(metrics)
        
            if response_is_success:
                is_success = True
                break

            time.sleep(2)
        
        if not is_success:
            raise Exception('Can not push metrics')

        self.metrics = []


class JobMetric():
    def __init__(self, name, **kwargs):
        self.name = name
        self.instance = kwargs.get('instance', None)
        self.env = kwargs.get('env', 'production')

        self.registry = MetricRegistry(
            env=self.env,
            labels={
                'name': "job-{}".format(name),
                'instance': self.instance,
                'env': self.env,
            }
        )

    def __enter__(self):
        return self.registry

    def __exit__(self, type, value, traceback):
        pass
        self.registry.push()

    def gauge(self, *args, **kwargs):
        self.registry.gauge(*args, **kwargs)

    def success(self):
        self.registry.gauge('job_up', value=1)
        self.registry.push()
    
    def failed(self):
        self.registry.gauge('job_up', value=0)
        self.registry.push()