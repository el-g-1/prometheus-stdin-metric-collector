from prometheus_client import start_http_server, Summary, Gauge
import sys, time
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY

gauge_dict = {}
num_collect = 0

class CustomCollector(object):
    def collect(self):
        global gauge_dict
        gfs = [gf for _, gf in gauge_dict.items()]
        global num_collect
        num_collect += 1
        if num_collect > 20:
            gauge_dict.clear()
            num_collect = 0
        return gfs

REGISTRY.register(CustomCollector())


def update_metrics(line_split):
    ts = None
    global gauge_dict
    for item in line_split:
        if item.startswith('ts:'):
            ts = int(item.split(':')[1]) // 1000
        else:
            parts = item.split(':')
            if len(parts) != 2:
                continue
            key, val = parts
            key_parts = key.split('|')
            labels = []
            label_names = None
            if len(key_parts) > 1:
                label_names = ['l' + str(i) for i in range(0, len(key_parts) - 1)]
                labels = key_parts[1:]
            metric_name = key_parts[0]
            if metric_name not in gauge_dict:
                gauge_dict[metric_name] = GaugeMetricFamily(metric_name, ('my ' + metric_name), labels=label_names)
            gauge_dict[metric_name].add_metric(labels, val, timestamp=ts)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    for line in sys.stdin:
        parts = line.split()
        for i, p in enumerate(parts):
            if p.startswith('ts:'):
                update_metrics(parts[i:])

