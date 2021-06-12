from prometheus_client import start_http_server, Summary, Gauge
import sys, time
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY

gauge_dict = {}

class CustomCollector(object):
    def collect(self):
        for _, gf in gauge_dict.items():
            yield gf

REGISTRY.register(CustomCollector())

# Create a metric to track time spent and requests made.


def update_metrics(line):
    line_split = line.split()
    ts = None
    for item in line_split:
        if item.startswith('ts:'):
            ts = int(item.split(':')[1]) // 1000
        else:
            if item.split(':')[0] not in gauge_dict:
                gauge_dict[item.split(':')[0]] = GaugeMetricFamily(item.split(':')[0], ('my ' + item.split(':')[0]))
            gauge_dict[item.split(':')[0]].add_metric([], item.split(':')[1], timestamp=ts)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    for line in sys.stdin:
        if line.startswith('ts:'):
            update_metrics(line)

