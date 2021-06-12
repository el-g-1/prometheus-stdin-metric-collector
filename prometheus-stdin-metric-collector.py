from prometheus_client import start_http_server
import sys
from prometheus_client.core import GaugeMetricFamily, REGISTRY


class CustomCollector(object):
    def __init__(self):
        self.gauge_dict = {}
        self.num_collect = 0

    def collect(self):
        gfs = [gf for _, gf in self.gauge_dict.items()]
        self.num_collect += 1
        if self.num_collect > 20:
            self.gauge_dict.clear()
            self.num_collect = 0
        return gfs

    def update_metrics(self, ts_part, line_split):
        ts = int(ts_part.split(':')[1]) // 1000
        for item in line_split:
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
            if metric_name not in self.gauge_dict:
                self.gauge_dict[metric_name] = GaugeMetricFamily(metric_name, ('my ' + metric_name),
                                                                 labels=label_names)
            self.gauge_dict[metric_name].add_metric(labels, val, timestamp=ts)


if __name__ == '__main__':
    collector = CustomCollector()
    REGISTRY.register(collector)
    # Start the server to expose the metrics
    start_http_server(8000)
    # Read metrics from stdin
    for line in sys.stdin:
        if line.startswith('ts:'):
            parts = line.split()
            collector.update_metrics(parts[0], parts[1:])
